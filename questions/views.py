# questions/views.py
import os
from collections import OrderedDict

from django.views.generic import DetailView, UpdateView, CreateView, RedirectView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django import forms


from braces.views import CsrfExemptMixin, LoginRequiredMixin, StaffuserRequiredMixin
from filebrowser.base import FileListing
from guardian.shortcuts import get_perms

from sendfile import sendfile

from core.models import ActivityLog
from core.mixins import CourseContextMixin, AccessRequiredMixin
from core.forms import PresetBookmarkForm
from notes.forms import UserNoteForm
from lessons.models import Lesson, Section
from courses.models import Course

from .models import TextQuestion, OptionQuestion, QuestionResponse, QuestionSet, UserWorksheetStatus, Option
from .forms import QuestionResponseForm, OptionQuestionUpdateForm, TextQuestionUpdateForm, OptionFormset, QuestionSetUpdateForm


def filter_filelisting_images(item):
    # item is a FileObject
    try:
        return item.filetype == "Image"
    except:
        return False


class QuestionAssetHandlerView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        asset = kwargs.pop('asset')
        abs_filename = os.path.join(
            os.path.join(settings.PDF_ROOT, asset)
        )
        return sendfile(request, abs_filename)


class WorksheetHomeView(LoginRequiredMixin, StaffuserRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'question_worksheet.html'

class WorksheetUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    model = QuestionSet
    template_name = 'activity_update.html'
    form_class = QuestionSetUpdateForm

    def get_success_url(self):
        return reverse_lazy('worksheet', args=[self.get_object().id])

    def get_context_data(self, **kwargs):
        context = super(WorksheetUpdateView, self).get_context_data(**kwargs)
        section_filter = forms.ModelChoiceField(
            queryset=Section.objects.filter(lesson=self.get_object().lesson))
        context['form'].fields['section'] = section_filter
        return context

class WorksheetLaunchView(LoginRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'question_worksheet.html'

    def get(self, request, *args, **kwargs):
        msg_detail = self.get_object().lesson.title
        ActivityLog(
            user=self.request.user, action='access-worksheet', message=self.request.path, message_detail=msg_detail).save()
        return HttpResponseRedirect(reverse('question_response', args=(self.kwargs['crs_slug'], self.get_object().id, 1)))



class QuestionResponseView(LoginRequiredMixin, AccessRequiredMixin, CourseContextMixin, CreateView):
    model = QuestionResponse
    template_name = 'question_sequence.html'
    form_class = QuestionResponseForm
    worksheet = None
    lesson = None
    next_question = None
    completion_status = None
    access_object = 'activity'

    def dispatch(self, *args, **kwargs):
        self.worksheet = get_object_or_404(
            QuestionSet, pk=self.kwargs['i'])
        self.next_question = self.worksheet.get_question_at_index(
            int(self.kwargs['j']) - 1)
        self.lesson = self.worksheet.lesson
        self.completion_status = self.request.user.completed_worksheets.filter(
            completed_worksheet=self.worksheet)

        return super(QuestionResponseView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs['crs_slug'])
        is_instructor = 'instructor' in get_perms(self.request.user, course)

        """ User has completed or is staff. No viewing restrictions enforced. """
        if self.request.user.is_staff or is_instructor or self.completion_status.count():
            if not self.next_question:
                """ No more questions. Send user to worksheet report. """
                return HttpResponseRedirect(reverse(
                    'worksheet_user_report', args=(self.kwargs['crs_slug'], self.worksheet.id, self.request.user.id)))

            return super(QuestionResponseView, self).get(request, *args, **kwargs)

        """ User is not staff but viewing restrictions are not enforced if response not required. """
        if self.next_question:
            if not self.next_question['question'].response_required:
                return super(QuestionResponseView, self).get(request, *args, **kwargs)

        """ Viewing restrictions enforced. """
        self.next_question = self.worksheet.get_next_question(self.request.user)

        """ If user's response queue is empty, user has completed worksheet, write completion status.
            Send user to worksheet report.
        """
        if not self.next_question:
            if not self.completion_status:
                UserWorksheetStatus(
                    user=self.request.user, completed_worksheet=self.worksheet).save()
                self.completion_status = True
                logpath = reverse('worksheet_report', args=(self.kwargs['crs_slug'], self.worksheet.id,))
                msg_detail = self.worksheet.lesson.title
                ActivityLog(user=self.request.user, action='completed-worksheet', message=logpath, message_detail=msg_detail).save()
                return HttpResponseRedirect(reverse('worksheet_user_report', args=(self.kwargs['crs_slug'], self.worksheet.id, self.request.user.id)))

        """
        Request parameter <j> is potentially overidden by next unanswered question
        in user's response queue.
        """
        if str(self.next_question['index']) != self.kwargs['j']:
            return HttpResponseRedirect(reverse('question_response', args=(self.kwargs['crs_slug'], self.worksheet.id, self.next_question['index'])))

        return super(QuestionResponseView, self).get(request, *args, **kwargs)

    def get_initial(self):
        try:
            self.initial['user'] = self.request.user
            self.initial['question'] = self.next_question['question']
        except:
            self.next_question = self.worksheet.get_next_question(
                self.request.user)
            self.initial['question'] = self.next_question['question']

        return self.initial

    def get_success_url(self):
        next_item = int(self.kwargs['j']) + 1
        course = self.kwargs['crs_slug']
        return reverse_lazy('question_response', args=[course, self.worksheet.id, next_item])

    def get_context_data(self, **kwargs):
        context = super(QuestionResponseView, self).get_context_data(**kwargs)
        current_question = self.initial['question']

        if not current_question:
            self.template_name = '404.html'
            return context

        # Tally
        tally = OrderedDict()
        for i in self.worksheet.get_ordered_question_list():

            try:
                response = i.user_response_object(
                    self.request.user).json_response()
                if i.check_answer(response):
                    tally[i] = 'success'
                else:
                    tally[i] = 'danger'
            except:
                tally[i] = 'default'

            if current_question.id == i.id:
                tally[i] = tally[i] + ' current'

        if self.request.user.is_staff:
            context['edit_url'] = current_question.get_edit_url(
                context['course'])

        question_index = self.worksheet.get_ordered_question_list().index(
            current_question) + 1

        """ 2015-04-14 -- disabling messages in question display until further notice
        initial_note_data = {}
        initial_note_data['content_type'] = ContentType.objects.get_for_model(
            current_question).id
        initial_note_data['object_id'] = current_question.id
        initial_note_data['creator'] = self.request.user
        initial_note_data['course_context'] = context['course']
        """

        try:
            bookmark = current_question.bookmarks.filter(
                creator=self.request.user).filter(course_context=context['course']).get()
            context['bookmarkform'] = PresetBookmarkForm(instance=bookmark)
            context['bookmark'] = bookmark
        except:
            bookmark = None
            initial_bookmark_data = {}
            initial_bookmark_data['mark_type'] = 'question'
            initial_bookmark_data['content_type'] = ContentType.objects.get_for_model(
                current_question).id
            initial_bookmark_data['object_id'] = current_question.id
            initial_bookmark_data['creator'] = self.request.user
            initial_bookmark_data['course_context'] = context['course']

            context['bookmarkform'] = PresetBookmarkForm(
                initial=initial_bookmark_data)
            context['bookmark'] = bookmark

        """
        context['noteform'] = UserNoteForm(initial=initial_note_data)
        context['note_list'] = current_question.notes.all().filter(
            course_context=context['course']).order_by('-created')
        """

        context['question'] = current_question
        context['question_position'] = question_index
        if question_index - 1 > 0:
            context['previous_position'] = question_index - 1
        if question_index + 1 <= len(list(tally)):
            context['next_position'] = question_index + 1
        context[
            'user_completed'] = self.completion_status or self.request.user.is_staff
        context['question_list'] = tally
        context['worksheet'] = self.worksheet
        context['instructor'] = self.request.user in context['course'].instructor_list() or self.request.user.is_staff

        if self.worksheet.lesson.id == 1:   # English math lesson.
            context['calculator'] = '/media/img/eng/ti-30xs-calculator-english.pdf'
            context['formula'] = '/media/pdf/eng-formula-page.pdf'
        elif self.worksheet.lesson.id == 5:  # Spanish math lesson
            context['calculator'] = '/media/pdf/eng/ti-30xs-calculator-english.pdf'
            context['formula'] = '/media/pdf/span-formula-page.pdf'

        # actionstr = 'access-question-' + current_question.get_question_type()
        # ActivityLog(
        #     user=self.request.user, action=actionstr, message=self.request.path).save()
        return context


class TextQuestionView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = TextQuestion
    template_name = 'question_view.html'

    def get_context_data(self, **kwargs):
        context = super(TextQuestionView, self).get_context_data(**kwargs)
        context['edit_url'] = self.get_object().get_edit_url(context['course'])
        context['sequence_url'] = self.get_object().get_sequence_url(
            context['course'])
        return context


class TextQuestionUpdateView(LoginRequiredMixin, CourseContextMixin, UpdateView):
    model = TextQuestion
    template_name = 'question_update.html'
    form_class = TextQuestionUpdateForm

    def get_success_url(self):
        course = self.kwargs['crs_slug']
        return reverse_lazy('text_question', args=[course, self.get_object().id])

    def get_context_data(self, **kwargs):
        context = super(
            TextQuestionUpdateView, self).get_context_data(**kwargs)
        lesson_filter = forms.ModelChoiceField(
            queryset=QuestionSet.objects.filter(lesson=self.get_object().question_set.lesson))
        context['form'].fields['question_set'] = lesson_filter
        context['filelisting'] = FileListing(
            'img', filter_func=filter_filelisting_images, sorting_by='date', sorting_order='desc').files_listing_filtered()

        return context

class TextQuestionDeleteView(LoginRequiredMixin, CourseContextMixin, DetailView):
    pass

class OptionQuestionView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = OptionQuestion
    template_name = 'question_view.html'

    def get_context_data(self, **kwargs):
        context = super(OptionQuestionView, self).get_context_data(**kwargs)
        context['options'] = self.get_object().options_list()
        context['edit_url'] = self.get_object().get_edit_url(context['course'])
        context['sequence_url'] = self.get_object().get_sequence_url(
            context['course'])
        return context



class OptionQuestionUpdateView(LoginRequiredMixin, CourseContextMixin, UpdateView):
    model = OptionQuestion
    template_name = 'question_update.html'
    form_class = OptionQuestionUpdateForm

    def get_success_url(self):
        course = self.kwargs['crs_slug']
        return reverse_lazy('option_question', args=[course, self.get_object().id])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        optionsform = OptionFormset(
            self.request.POST, instance=self.get_object())
        if form.is_valid() and optionsform.is_valid():
            return self.form_valid(form, optionsform)
        else:
            return self.form_invalid(form, optionsform)

    def form_valid(self, form, optionsform):
        optionsform.save()
        return super(OptionQuestionUpdateView, self).form_valid(form)

    def form_invalid(self, form, optionsform):
        return self.render_to_response(
            self.get_context_data(form=form, optionsform=optionsform))

    def get_context_data(self, **kwargs):
        context = super(
            OptionQuestionUpdateView, self).get_context_data(**kwargs)
        context['optionsform'] = OptionFormset(instance=self.get_object())
        lesson_filter = forms.ModelChoiceField(
            queryset=QuestionSet.objects.filter(lesson=self.get_object().question_set.lesson))
        context['form'].fields['question_set'] = lesson_filter
        context['filelisting'] = FileListing(
            'img', filter_func=filter_filelisting_images, sorting_by='date', sorting_order='desc').files_listing_filtered()

        return context


class UserReportView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = QuestionSet
    template_name = 'question_worksheet_report.html'

    def get_context_data(self, **kwargs):
        context = super(UserReportView, self).get_context_data(**kwargs)
        # if not self.request.user.has_perm('instructor') and self.request.user.id not self.kwargs['user']:
        #     raise PermissionDeniedError

        user = User.objects.get(pk=self.kwargs['user'])
        worksheet = self.get_object()
        context['worksheet'] = worksheet
        context['numquestions'] = worksheet.get_num_questions()

        report = worksheet.get_user_responses(
           user, worksheet.get_ordered_question_list(), context['course'])
        context['report'] = report['report']

        context['correct'] = report['correct']
        context['grade'] = report['grade']
        return context


class FullReportView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = QuestionSet
    template_name = 'question_worksheet_report.html'

    def get_context_data(self, **kwargs):
        context = super(FullReportView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        context['worksheet'] = worksheet
        context['numquestions'] = worksheet.get_num_questions()
        context['reports'] = worksheet.get_all_responses(context['course'])
        # context['grade'] = correct/context['numquestions']
        # print context['reports'][4]
        return context


class LessonKeyView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = Lesson
    template_name = 'question_worksheet_key.html'

    def get_context_data(self, **kwargs):
        context = super(LessonKeyView, self).get_context_data(**kwargs)
        key = []
        worksheets = self.get_object().worksheets.all()
        for i in worksheets:
            k_items = []
            for question in i.get_ordered_question_list():
                try:
                    if question.display_key_file:
                        answer = '<a href="' + question.display_key_file.url + '">key</a>'
                    elif question.get_question_type() == 'option':
                        corrects = question.correct_answer()
                        answer = ''
                        for x in corrects:
                            answer += Option.objects.get(pk=x).display_text
                    else:
                        answer = question.correct_answer()

                    if answer:
                        k_items.append((question.display_text, answer))
                except Exception as e:
                    print e
            key.append((i, k_items))
        context['worksheets'] = key
        return context

class WorksheetKeyView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = QuestionSet
    template_name = 'question_worksheet_key.html'

    def get_context_data(self, **kwargs):
        context = super(WorksheetKeyView, self).get_context_data(**kwargs)
        key = []

        k_items = []
        for question in self.get_object().get_ordered_question_list():
            try:
                if question.display_key_file:
                    answer = '<a href="' + question.display_key_file.url + '">key</a>'
                elif question.get_question_type() == 'option':
                    corrects = question.correct_answer()
                    answer = ''
                    for x in corrects:
                        answer += Option.objects.get(pk=x).display_text
                else:
                    answer = question.correct_answer()

                if answer:
                    k_items.append((question.display_text, answer))
            except Exception as e:
                print e

        key.append((self.get_object(), k_items))

        context['worksheets'] = key
        return context



