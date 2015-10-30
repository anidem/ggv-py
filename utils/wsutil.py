import os, json, sys, csv
from collections import OrderedDict

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.text import slugify

from questions.models import *
from slidestacks.models import *
from lessons.models import *

idmap = {u'0': u'2', u'': u'2', u'1269': u'614', u'812': u'470', u'815': u'471', u'817': u'472', u'1798': u'793', u'1399': u'659', u'719': u'443', u'715': u'442', u'1790': u'792', u'712': u'441', u'1266': u'613', u'1492': u'717', u'1495': u'718', u'1396': u'658', u'1498': u'719', u'1702': u'761', u'1704': u'762', u'1707': u'763', u'1061': u'553', u'1528': u'729', u'1064': u'554', u'1067': u'555', u'1667': u'748', u'1664': u'747', u'1660': u'746', u'1087': u'562', u'1084': u'561', u'1081': u'560', u'1122': u'573', u'1125': u'574', u'1018': u'537', u'1015': u'536', u'1401': u'660', u'1407': u'662', u'1012': u'535', u'1404': u'661', u'1234': u'605', u'1231': u'604', u'1334': u'638', u'1337': u'639', u'1332': u'637', u'1545': u'734', u'901': u'500', u'904': u'501', u'908': u'502', u'1510': u'724', u'1534': u'731', u'1245': u'606', u'1531': u'730', u'646': u'418', u'1249': u'607', u'856': u'485', u'851': u'483', u'853': u'484', u'859': u'486', u'1622': u'696', u'1625': u'697', u'1628': u'698', u'740': u'451', u'743': u'452', u'746': u'453', u'749': u'454', u'1050': u'548', u'1052': u'549', u'1054': u'550', u'1057': u'551', u'1190': u'596', u'1192': u'597', u'1195': u'598', u'1197': u'599', u'1697': u'759', u'1693': u'758', u'1691': u'757', u'1757': u'780', u'1755': u'779', u'1752': u'778', u'1099': u'565', u'1699': u'760', u'1175': u'592', u'1172': u'591', u'1271': u'615', u'1274': u'616', u'1179': u'593', u'1277': u'617', u'1285': u'620', u'1280': u'618', u'1282': u'619', u'947': u'514', u'944': u'513', u'1288': u'621', u'941': u'512', u'1472': u'709', u'1470': u'708', u'1476': u'710', u'1474': u'711', u'1059': u'552', u'1573': u'679', u'684': u'432', u'1478': u'712', u'1570': u'678', u'1577': u'680', u'680': u'430', u'682': u'431', u'1304': u'627', u'1306': u'628', u'1301': u'626', u'1309': u'629', u'1373': u'650', u'938': u'511', u'1377': u'651', u'932': u'509', u'935': u'510', u'829': u'476', u'826': u'475', u'820': u'473', u'823': u'474', u'709': u'440', u'704': u'438', u'707': u'439', u'702': u'437', u'1482': u'714', u'1480': u'713', u'1484': u'715', u'1489': u'716', u'1713': u'765', u'796': u'465', u'794': u'464', u'1716': u'766', u'791': u'463', u'1719': u'767', u'798': u'466', u'1658': u'745', u'1652': u'742', u'1650': u'741', u'1656': u'744', u'1654': u'743', u'1138': u'578', u'1738': u'773', u'1131': u'576', u'1134': u'577', u'1384': u'654', u'1437': u'672', u'1435': u'671', u'1431': u'670', u'1731': u'771', u'1382': u'653', u'1009': u'534', u'1006': u'533', u'1003': u'532', u'1000': u'531', u'1128': u'575', u'1225': u'602', u'1223': u'601', u'1221': u'600', u'1340': u'640', u'1343': u'641', u'1346': u'642', u'1228': u'603', u'977': u'523', u'976': u'522', u'978': u'524', u'657': u'422', u'654': u'421', u'1501': u'721', u'1507': u'722', u'1504': u'720', u'651': u'420', u'868': u'490', u'860': u'487', u'863': u'488', u'864': u'489', u'885': u'495', u'888': u'496', u'1619': u'695', u'1616': u'694', u'1613': u'693', u'1610': u'692', u'774': u'461', u'1043': u'545', u'1045': u'546', u'1048': u'547', u'1682': u'753', u'1684': u'754', u'1687': u'755', u'1689': u'756', u'1763': u'782', u'1760': u'781', u'1766': u'783', u'1142': u'580', u'1140': u'579', u'1147': u'582', u'1144': u'581', u'668': u'426', u'1263': u'612', u'665': u'425', u'1260': u'611', u'662': u'424', u'660': u'423', u'693': u'434', u'691': u'433', u'696': u'435', u'1543': u'732', u'1541': u'733', u'699': u'436', u'1548': u'735', u'1465': u'707', u'1463': u'706', u'994': u'529', u'997': u'530', u'1314': u'631', u'991': u'528', u'1311': u'630', u'1318': u'632', u'1787': u'791', u'1295': u'624', u'929': u'508', u'920': u'506', u'1387': u'655', u'1380': u'652', u'926': u'507', u'832': u'477', u'837': u'479', u'834': u'478', u'839': u'480', u'784': u'462', u'1641': u'703', u'1728': u'770', u'1725': u'769', u'1722': u'768', u'1743': u'775', u'1779': u'788', u'1421': u'667', u'1588': u'683', u'1427': u'669', u'1580': u'681', u'1587': u'684', u'1584': u'682', u'1039': u'544', u'734': u'449', u'737': u'450', u'1031': u'541', u'1037': u'543', u'1034': u'542', u'1359': u'646', u'1353': u'644', u'1350': u'643', u'1356': u'645', u'964': u'520', u'962': u'519', u'969': u'521', u'1107': u'568', u'1104': u'567', u'1457': u'705', u'1519': u'726', u'1101': u'566', u'1516': u'725', u'1459': u'704', u'1513': u'723', u'879': u'494', u'875': u'493', u'872': u'491', u'873': u'492', u'890': u'497', u'893': u'498', u'898': u'499', u'1150': u'583', u'649': u'419', u'1152': u'584', u'1601': u'689', u'1604': u'690', u'1607': u'691', u'808': u'469', u'803': u'467', u'806': u'468', u'769': u'460', u'762': u'458', u'1781': u'789', u'1784': u'790', u'765': u'459', u'1774': u'786', u'1776': u'787', u'1771': u'785', u'1078': u'559', u'1076': u'558', u'1072': u'557', u'1113': u'570', u'1070': u'556', u'1679': u'752', u'1674': u'750', u'1677': u'751', u'1671': u'749', u'1096': u'564', u'1090': u'563', u'1158': u'586', u'1155': u'585', u'677': u'429', u'671': u'427', u'673': u'428', u'1290': u'622', u'1551': u'736', u'1554': u'737', u'1557': u'738', u'1559': u'739', u'1418': u'666', u'1410': u'663', u'1413': u'664', u'1416': u'665', u'1322': u'633', u'988': u'527', u'1327': u'635', u'1324': u'634', u'981': u'525', u'985': u'526', u'1525': u'728', u'1255': u'609', u'1253': u'608', u'1522': u'727', u'914': u'504', u'917': u'505', u'911': u'503', u'1392': u'657', u'1258': u'610', u'1390': u'656', u'1423': u'668', u'847': u'482', u'843': u'481', u'1631': u'699', u'1634': u'700', u'1637': u'702', u'1638': u'701', u'1734': u'772', u'732': u'448', u'753': u'455', u'1329': u'636', u'756': u'456', u'759': u'457', u'1595': u'686', u'1594': u'687', u'1591': u'685', u'1598': u'688', u'1445': u'674', u'1024': u'539', u'1027': u'540', u'1021': u'538', u'1185': u'595', u'1182': u'594', u'727': u'446', u'724': u'445', u'722': u'444', u'1749': u'777', u'1746': u'776', u'1740': u'774', u'729': u'447', u'1166': u'589', u'1160': u'587', u'1163': u'588', u'1169': u'590', u'959': u'518', u'950': u'515', u'953': u'516', u'956': u'517', u'1110': u'569', u'1298': u'625', u'1769': u'784', u'1116': u'571', u'1119': u'572', u'1293': u'623', u'1562': u'740', u'1565': u'676', u'1449': u'675', u'1567': u'677', u'1710': u'764', u'1803': u'794', u'1366': u'648', u'1362': u'647', u'1440': u'673', u'1369': u'649'}
# json_dir = os.path.abspath('/Users/rmedina/Desktop/ggvworksheet-conversion/worksheet-downloads/worksheets-social/csvdir/SOCIAL\ \(ENG\)\ QUESTIONS\ INPUT')


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

def imgmap():
    imgmaplist = {}
    files = []
    for fstr in os.listdir(json_dir):
        if fstr != '.DS_Store':
            files.append(fstr)

    for f in files:
        # print 'READING FILE: ', f
        json_file = open('%s/%s' % (json_dir, f))
        json_data = json_file.read()
        data = json.loads(json_data) # deserialises it

        WID = None
        ws = None
        questions = None
        for i in data:
            if i.get('WID') != '':
                WID = i.get('WID')
                ws = QuestionSet.objects.get(pk=idmap[WID])
                # print 'READING DB worksheet: ', ws.id

                questions = ws.get_ordered_question_list()

            try:
                display_order = i.get('QUESTION DISPLAY ORDER')
                display_image = slugify(i.get('IMAGE'))

                if display_image:
                    for q in questions:
                        if str(q.display_order) == display_order:
                            # qimg = {'question': q.id, 'name': slugify(display_image)}
                            imgmaplist[q.id] = slugify(display_image)
                            print '%s, %s' %  (q.id, display_image)



            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
                continue

        json_file.close()

    return imgmaplist

def slug_files(path):#filter(os.path.isdir, os.listdir(os.getcwd()))
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

def slug_curr_dir():#filter(os.path.isdir, os.listdir(os.getcwd()))
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


def import_json_questions(json_dir=None):
    optsmap ={'A': '1', 'B': '2', 'C': '3', 'D': '4' }
    files = []
    # json_dir = os.path.abspath('/Users/rmedina/Desktop/ggvworksheet-conversion/worksheet-downloads/worksheets-math/jsondir')
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

        # Get the worksheet once per file.
        if data[0].get('WID') != '':
                WID = data[0].get('WID')
                print 'processing worksheet id: ', WID
                try:
                    worksheet_obj = QuestionSet.objects.get(pk=idmap[WID])
                except:
                    # This need to be configured for the desination lesson and section.
                    lesson = Lesson.objects.get(pk=1)
                    section = Section.objects.get(pk=131)
                    worksheet_obj =  QuestionSet(lesson=lesson, section=section,title=WID, instructions='Add instructions here.', display_order=0, activity_type='worksheet')
                    worksheet_obj.save()
                    print 'Worksheet does not exist: Worksheet ADDED: ', worksheet_obj

        # Iterate over each question --> i = json question object
        for i in data:
            try:
                if i.get('IMAGE') != '':
                    imgpath = 'img/' + i.get('IMAGE')
                    # imgpath = 'img/' + slugify(i.get('IMAGE')) + '.png'
                else:
                    imgpath = ''
                # imgpath = i.get('IMAGE')
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
                        except Exception as e:
                            print '%s (%s)' % (e.message, type(e))
                            print 'VALUE=*%s*'% (v)
                            print 'WID:', WID
                        opt.save()

            except Exception as e:
                print e

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







