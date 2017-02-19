import os, json, sys, csv
from collections import OrderedDict

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.text import slugify

from questions.models import *
from slidestacks.models import *
from lessons.models import *


def convert_text_to_option(source_pk=None):
    try:
        s = TextQuestion.objects.get(pk=source_pk)
        t = OptionQuestion()
        t.display_text = s.display_text
        t.question_set = s.question_set
        t.display_order = s.display_order
        t.display_image = s.display_image
        t.display_pdf = s.display_pdf
        t.response_required = s.response_required
        t.save()
        s.delete()
        return t
    except Exception as e:
        print e
        return None

def convert_option_to_text(source_pk=None):
    try:
        s = OptionQuestion.objects.get(pk=source_pk)
        t = TextQuestion()
        t.display_text = s.display_text
        t.question_set = s.question_set
        t.display_order = s.display_order
        t.display_image = s.display_image
        t.display_pdf = s.display_pdf
        t.response_required = s.response_required
        t.save()
        s.delete()
        return t
    except Exception as e:
        print e
        return

class worksheetvalidator(TemplateView):
    template_name = 'question_validator.html'
    def get_context_data(self, **kwargs):
        context = super(worksheetvalidator, self).get_context_data(**kwargs)
        worksheets = QuestionSet.objects.all()
        deactivated = Lesson.objects.get(pk=10)
        failures = []
        for i in worksheets:
            if not i.get_ordered_question_list():
                i.lesson = deactivated
                i.section = None
                i.save()
                failures.append(i)
        context['worksheets'] = worksheets
        context['failures'] = failures
        return context

def csvutil(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['question id', 'lesson', 'sheet', 'order', 'type', 'image'])
    worksheets = QuestionSet.objects.all()
    for sheet in worksheets:
        for q in sheet.get_ordered_question_list():
            if q.display_image != '':
                writer.writerow([q.id, sheet.lesson, sheet, q.display_order, q.get_question_type(), q.display_image])

    return response

def csvutilslides(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="slidestacks.csv"'
    writer = csv.writer(response)
    writer.writerow(['slidestack id', 'lesson', 'slidestack title', 'order', 'asset'])
    slidestacks = SlideStack.objects.all().order_by('section__lesson', 'section__display_order', 'display_order')
    for stack in slidestacks:
        # print stack.section, stack
        writer.writerow([stack.id, stack.lesson, stack, stack.display_order, stack.asset])

    return response

def imgmapset():
    pass

def imgr(q, r):
    opts=OptionQuestion.objects.all()
    txts=TextQuestion.objects.all()
    t = txts.filter(display_image__contains=q)
    for i in t:
        i.display_image = r
        i.save()

    o = opts.filter(display_image__contains=q)
    for i in o:
        i.display_image = r
        i.save()
    return



def slug_files(path):# filter(os.path.isdir, os.listdir(os.getcwd()))
    input_dir = os.path.abspath(path)
    files = []
    for fstr in filter(os.path.isfile, os.listdir(input_dir)):
        if fstr != '.DS_Store':
            files.append(fstr)
            # print fstr

    # rename each file by slugifying it.
    for i in files:
        # print i
        os.rename(
            os.path.join(input_dir, i),
            os.path.join(
                input_dir,
                slugify(
                    unicode(i.replace('(Web)',''), errors='replace')
                )
            )
        )

def slug_curr_dir(): # filter(os.path.isdir, os.listdir(os.getcwd()))
    input_dir = os.path.abspath('.')
    files = []
    for fstr in filter(os.path.isdir, os.listdir(input_dir)):
        files.append(fstr)

    # rename each file by slugifying it.
    for i in files:
        # print i
        os.rename(
            os.path.join(input_dir, i),
            os.path.join(
                input_dir,
                slugify(
                    unicode(i.replace('(Web)',''), errors='replace')
                )
            )
        )

def update_worksheet_json_questions_from_file(json_dir=None, json_file_name=None, wid=None, fake=False):

    # TODO
    pass


def import_new_json_questions_from_file(json_dir=None, json_file_name=None, lid=None, sid=None, fake=False):
    """Introduced 2017-02-18 to create new worksheet from json file.
        
        csvcut used to generate json file
        
        References new column layout:
        
        csvcut -c "title","order","question","image","type","correct","option 1","option 2","option 3","option 4" ./sample.csv | csvjson -i 4 > sample.json
        
        "title","order","question","image","type","correct","option 1","option 2","option 3","option 4"
    """
    optsmap ={'A': '1', 'B': '2', 'C': '3', 'D': '4', 'a': '1', 'b': '2', 'c': '3', 'd': '4' }

    json_file = open('%s/%s' % (json_dir, json_file_name)) 
    data = json.loads(json_file.read()) # deserializes it
    print 'PROCESSING ==>', json_file
    json_file.close()

    worksheet_title = 'no title'
    worksheet_obj = None

    # Setup a new worksheet
    if data[0].get('title') != '':
        worksheet_title = data[0].get('title')
    
    print 'NEW WORKSHEET TITLE ==> ', worksheet_title
    lesson = Lesson.objects.get(pk=lid)
    
    print 'WORKSHEET LESSON ==> ', lesson.id, lesson.title
    section = Section.objects.get(pk=sid)
    
    print 'WORKSHEET SECTION ==> ', section.id, section.title
    
    worksheet_obj = QuestionSet(lesson=lesson, section=section, title=worksheet_title, instructions='Add instructions here.', display_order=0, activity_type='worksheet')
    if not fake: worksheet_obj.save()

    print 'NEW WORKSHEET CREATED ==> ', worksheet_obj.id, worksheet_obj.title

    # Iterate over each question --> i = json question object
    for i in data:
        try:
            if i.get('type') == 'text':
                question = TextQuestion()
                question.display_text = i.get('question')
                question.display_order = i.get('order')
                question.correct = i.get('correct')
                if i.get('image') == '':
                    imgpath = ''
                elif i.get('image')[-3:] == 'pdf':
                    question.display_pdf = 'pdf/' + i.get('image')
                else:
                    question.display_image = 'img/' + i.get('image')
                
                question.question_set = worksheet_obj
                if not fake: question.save()
            else:
                question = OptionQuestion()
                question.display_text = i.get('question')
                question.display_order = i.get('order')
                if i.get('image') == '':
                    imgpath = ''
                elif i.get('image')[-3:] == 'pdf':
                    question.display_pdf = 'pdf/' + i.get('image')
                else:
                    question.display_image = 'img/' + i.get('image')

                question.input_select = i.get('type')
                question.question_set = worksheet_obj
                if not fake: question.save()
                
                corstr =  i.get('correct')
                corlist = corstr.split(',')

                # retrieve the list of options (option 1, option 2, ...)
                opts = dict((k, v) for k, v in sorted(i.items()) if k.startswith('option'))
                
                # process each retrieved option
                for k, v in opts.items():
                    try:
                        order = k[7:] # get the number portion of the key: e.g.,option 1 --> 1
                        opt = Option()
                        opt.display_text = v
                        opt.display_order = order
                        for c in corlist:
                            try:
                                opt.correct = order == optsmap[c]
                            except:
                                opt.correct = order == c

                        opt.question = question
                    except Exception as e:
                        print '%s (%s)' % (e.message, type(e))
                        print 'VALUE=*%s*'% (v)
                        print 'WORKSHEET:', worksheet_obj
                    
                    if not fake: opt.save()

        except Exception as e:
            print e

        # except ValueError:
        #     print '[%s] not saved'% i.get('QUESTION')
        #     continue
        # except KeyError as e:
        #     print '%s (%s)' % (e.message, type(e))
        #     # print e.message
        #     continue



        # seqitem = QuestionSequenceItem(content_object=question, question_sequence=seq)
        # seqitem.save()

        try:
            print 'Updated %s with %s' % (worksheet_obj.title, question.display_text[:10])
             
        except Exception as e:
            type, value, traceback = sys.exc_info()
            print traceback, value, i

    
    return




def json_repair_questions(json_dir=None):
    worksheet_repairs=[782, 783, 785, 786, 787, 788, 789, 790, 791, 792]
    optsmap ={'A': '1', 'B': '2', 'C': '3', 'D': '4' }
    files = []
    # json_dir = os.path.abspath('/Users/rmedina/Desktop/ggvworksheet-conversion/worksheet-downloads/worksheets-math/jsondir')
    imgmaprep = {
        '782': 'img/span/5-span-commas/span-comma-rule-2-1-32.png',
        '783': 'img/span/5-span-commas/span-comma-rule-3-1-28.png',
        '785': 'img/span/5-span-commas/span-comma-rule-4-1-32.png',
        '786': 'img/span/5-span-commas/span-comma-rules-denver-1-54.png',
        '787': '',
        '788': '',
        '789': '',
        '790': '',
        '791': '',
        '792': '',
    }


    for fstr in os.listdir(json_dir):
        if fstr != '.DS_Store':
            files.append(fstr)

    for f in files:
        print f
        json_file = open('%s/%s' % (json_dir, f))
        json_data = json_file.read()
        data = json.loads(json_data) # deserialises it

        WID = None
        worksheet_obj = None

        # Get the worksheet id once per file.
        if data[0].get('WID') != '':
                WID = data[0].get('WID')
                print 'processing worksheet id: ', WID
                try:
                    worksheet_obj = QuestionSet.objects.get(pk=WID)
                except:
                    print 'Worksheet does not exist: ', worksheet_obj
                    raise Exception

        # Iterate over each question --> i = json question object
        for i in data:
            try:
                # if i.get('IMAGE') != '':
                #     imgpath = 'img/' + slugify(i.get('IMAGE')) + '.png'
                # else:
                #     imgpath = ''
                # imgpath = i.get('IMAGE')
                if imgmaprep[WID]:
                    imgpath = imgmaprep[WID]
                else:
                    imgpath = None

                if i.get('SELECT TYPE') == 'text':
                    question = TextQuestion()
                    question.display_text = i.get('QUESTION')
                    question.display_order = i.get('QUESTION DISPLAY ORDER')
                    question.correct = i.get('CORRECT ANSWER')
                    question.display_image = imgpath
                    question.question_set = worksheet_obj
                    question.save()
                else:
                    question = OptionQuestion()
                    question.display_text = i.get('QUESTION')
                    question.display_order = i.get('QUESTION DISPLAY ORDER')
                    question.display_image = imgpath
                    question.input_select = i.get('SELECT TYPE')
                    question.question_set = worksheet_obj
                    question.save()
                    corstr =  i.get('CORRECT ANSWER')
                    corlist = corstr.split(',')

                    opts = dict((k, v) for k, v in sorted(i.items()) if k.startswith('option'))
                    for k, v in opts.items():
                        try:
                            order = k[7:] # get the number portion of the key: e.g.,option 1 --> 1
                            opt = Option()
                            opt.display_text = v
                            opt.display_order = order
                            for c in corlist:
                                try:
                                    opt.correct = order == optsmap[c]
                                except:
                                    opt.correct = order == c

                            opt.question = question
                            opt.save()
                        except Exception as e:
                            print '%s (%s)' % (e.message, type(e))
                            print 'VALUE=*%s*'% (v)
                            print 'WID:', WID

                question.question_set = worksheet_obj
                question.save()

            except ValueError:
                print '[%s] not saved'% i.get('QUESTION')
                continue
            except KeyError as e:
                print '%s (%s)' % (e.message, type(e))
                # print e.message
                continue



            # seqitem = QuestionSequenceItem(content_object=question, question_sequence=seq)
            # seqitem.save()

            # print question
            print 'updated %s with %s' % (worksheet_obj, question)
        json_file.close()


    return







