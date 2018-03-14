# -*- coding: utf-8 -*-

from backports import csv
import io

from questions.models import *
from lessons.models import *

data = [
    {'ws': 150, 'lesson': 1, 'csv': 'eng math.csv'},{'ws': 151, 'lesson': 2, 'csv': 'eng science.csv'},{'ws': 152, 'lesson': 3, 'csv': 'eng social.csv'},{'ws': 153, 'lesson': 4, 'csv': 'eng language.csv'},{'ws': 154, 'lesson': 5, 'csv': 'span math.csv'},{'ws': 155, 'lesson': 6, 'csv': 'span science.csv'},{'ws': 156, 'lesson': 7, 'csv': 'span social.csv'},{'ws': 157, 'lesson': 8, 'csv': 'span language.csv'}
]


def run():
    for item in data:
        do_mapping(item=item)


def do_mapping(item=None):
    lesson = Lesson.objects.get(pk=item['lesson'])
    pretest = QuestionSet.objects.get(pk=item['ws'])
    questions = pretest.get_ordered_question_list()
    mapping = get_map(f=item['csv'])
    print lesson.title, '\n================================='
    
    for question, module_pk in mapping:
        pretest_q = questions[question-1]
        related_m = Section.objects.get(pk=module_pk)
        pretest_q.content_area = related_m
        pretest_q.save()
        print question, pretest_q.pk, '==>', pretest_q.content_area.title
        

def get_map(f=None):
    file = './ggvutils/module_question_mapper/'+f
    mod_questions = []
    with io.open(file, newline='', encoding='utf-8') as csvfile:
        for row in csv.reader(csvfile):
            mod_questions.append((int(row[0]), int(row[4])))
    return mod_questions

def get_module(modules=None, q=None):
    for module_obj in modules:
        mod_title = module_obj.title.lower()
        mod_query = q.lower()
        if mod_query in mod_title:
            return module_obj
    return None

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')