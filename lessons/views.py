# This Python file uses the following encoding: utf-8

# lessons/views.py
from django import forms
from django.db.models import Q
from django.views.generic import DetailView, UpdateView, ListView, TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from core.mixins import CourseContextMixin, AccessRequiredMixin, PrivelegedAccessMixin
from core.models import ActivityLog, Bookmark, BOOKMARK_TYPES, SitePage
from core.utils import activity_stat_worksheet, activity_stat_slides
from .models import Lesson, Section
from questions.models import Option


class LessonView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'
    access_object = 'lesson'

    def get(self, request, *args, **kwargs):
        # provides a link to last activity in this lesson.
        acts = request.user.activitylog.all().filter(Q(action='login') | Q(message_detail=self.get_object().title))
        last_lesson_act = acts.filter(message_detail=self.get_object().title)[:1]
        # print 'CURRENT STATE', self.get_object(), self.request.user
        # for i in acts: print i.timestamp, i.action, i.message_detail
        # print 'LAST ACTIVITY==>', last_lesson_act

        self.last_activity = ''
        if acts and acts[0].action == 'login':
            # No events related to current lesson ocurred after login event            
            if last_lesson_act: # Grab the most recent...build notification message
                
                self.last_activity = last_lesson_act[0].message
                
                if self.request.user.ggvuser.language_pref == 'spanish':
                    msg = u'<p class="text-center">¿Continuar con la ultima actividad?</p>'
                else: 
                    msg = u'<p class="text-center">Continue where you left off?</p>'
                
                msg += u'<p class="text-center">' + self.last_activity + '</p>'
                messages.info(self.request, msg, extra_tags='safe')
        
        if not last_lesson_act:
            # No prior lesson related events exist. Activate preamble.
            msg_url = reverse('lesson_preamble', args=[self.kwargs['crs_slug'],self.get_object().pk])
            message = u'<a href="' + msg_url + u'">' + self.get_object().title + u'</a>'
            ActivityLog(user=request.user, action='preamble', message=message, message_detail=self.get_object().title).save()
            self.last_activity = 'preamble'  # activate modal in lesson view
            
            # turn this on if we simply want to redirect
            # return redirect('lesson_preamble', crs_slug=self.kwargs['crs_slug'], pk=self.get_object().pk)                       

        return super(LessonView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()

        opts = dict(BOOKMARK_TYPES)
        for i, j in opts.items():
            if self.request.user.ggvuser.language_pref == 'spanish':
                opts[i] = j.split(',')[1]
            else:
                opts[i] = j.split(',')[0]

        context['bookmark_type_opts'] = opts

        activity_list = []
        bookmarks = Bookmark.objects.filter(creator=self.request.user).filter(course_context=context['course'])

        completions = self.request.user.completed_worksheets.all()
        for i in lesson.activities():
            activity_type = ContentType.objects.get_for_model(i).id
            bookmark = None
            bookmark_label = ''
            bookmark_id = ''
            bookmark_type = 'none'
            try:
                bookmark = bookmarks.filter(content_type=activity_type).get(object_id=i.id)

                label = bookmark.get_mark_type_display()
                # if lesson.language == 'span':
                if self.request.user.ggvuser.language_pref == 'spanish':
                    label = label.split(',')[1]
                else:
                    label = label.split(',')[0]

                bookmark_label = label
                bookmark_id = bookmark.id
                bookmark_type = bookmark.mark_type

                # bookmarkform = BookmarkForm(instance=bookmark)

            except:
                pass

            a = {}
            a['act'] = i
            a['act_type_id'] = activity_type
            a['note'] = None
            # a['bookmarkform'] = bookmarkform
            a['bookmark'] = bookmark
            a['bookmark_id'] = bookmark_id
            a['bookmark_label'] = bookmark_label
            a['bookmark_type'] = bookmark_type
            a['date'] = None
            if activity_type == 13:  # worksheet activity
                a['score'] = completions.filter(completed_worksheet=i)

            activity_list.append(a)

        #  build user activity stats info
        context['worksheets_stat'] = activity_stat_worksheet(self.request.user, lesson)
        context['slides_stat'] = activity_stat_slides(self.request.user, lesson)

        context['acts'] = activity_list
        context['sections'] = lesson.sections.all()
        context['is_staff'] = self.request.user.is_staff
        context['instructor'] = self.request.user in context['course'].instructor_list() or self.request.user.is_staff
        context['language_pref'] = self.request.user.ggvuser.language_pref

        context['last_activity'] = self.last_activity


        subject = self.get_object().subject
        plan = subject+'-educational-plan'
        guide = subject+'-guide'
        steps = 'steps-to-completion'

        # uncomment after spanish materials have converted
        # if self.request.user.ggvuser.language_pref == 'spanish':
        #     plan += '-span'
        #     guide += '-span'
        #     steps += '-span'

        context['plan'] = SitePage.objects.get(slug=plan)
        context['guide'] = SitePage.objects.get(slug=guide)
        context['steps'] = SitePage.objects.get(slug=steps)



        return context


class SectionUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, CourseContextMixin, UpdateView):
    model = Section
    template_name = 'activity_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('lesson', args=[self.kwargs['crs_slug'], self.get_object().lesson.id])

    def get_context_data(self, **kwargs):
        context = super(SectionUpdateView, self).get_context_data(**kwargs)
        return context


class LessonPreambleView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = Lesson
    template_name = 'lesson_preamble_page.html'

    def get_context_data(self, **kwargs):
        context = super(LessonPreambleView, self).get_context_data(**kwargs)
        subject = self.get_object().subject
        plan = subject+'-educational-plan'
        guide = subject+'-guide'
        steps = 'steps-to-completion'

        # uncomment after spanish materials have converted
        # if self.request.user.ggvuser.language_pref == 'spanish':
        #     plan += '-span'
        #     guide += '-span'
        #     steps += '-span'

        context['plan'] = SitePage.objects.get(slug=plan)
        context['guide'] = SitePage.objects.get(slug=guide)
        context['steps'] = SitePage.objects.get(slug=steps)



        return context




