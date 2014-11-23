from django.conf.urls import patterns, include, url
from django.contrib import admin
# admin.autodiscover()

from core.views import IndexView, HomeView
from notes.views import NoteCreateView, NoteView
from courses.views import CourseView
from lessons.views import LessonView
from questions.views import WorksheetHomeView, QuestionResponseView, ImportJsonQuestion, OptionQuestionUpdateView, TextQuestionUpdateView, OptionQuestionView, TextQuestionView
from slidestacks.views import SlideStackInitView, SlideStackView


urlpatterns = patterns('',

# GGV
    url(r'^ggv/(?P<slug>[-\w]+)/$', CourseView.as_view(), name='course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/lesson/(?P<pk>\d+)$', LessonView.as_view(), name='lesson'),
    
# GGV lesson activities
    url(r'^ggv/slidestack-init/(?P<pk>\d+)', SlideStackInitView.as_view(), name='slidestack_init'),
    url(r'^ggv/slidestack/(?P<pk>\d+)', SlideStackView.as_view(), name='slidestack'),
    
    url(r'^ggv/worksheet/(?P<i>\d+)/(?P<j>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    
    url(r'^ggv/questions/textquestions/(?P<pk>\d+)/$', TextQuestionView.as_view(), name='text_question'),
    url(r'^ggv/questions/textquestions/edit/(?P<pk>\d+)/$', TextQuestionUpdateView.as_view(), name='text_question_update'),
    
    url(r'^ggv/questions/optionquestions/(?P<pk>\d+)/$', OptionQuestionView.as_view(), name='option_question'),
    url(r'^ggv/questions/optionquestions/edit/(?P<pk>\d+)/$', OptionQuestionUpdateView.as_view(), name='option_question_update'),

# GGV components
    url(r'^ggv/note/(?P<pk>\d+)/$', NoteView.as_view(), name='view_note'),
    url(r'^ggv/note/add/$', NoteCreateView.as_view(), name='create_note'),


# Utility - NON Production use only!

    # url(r'^ggv/import/$', ImportJsonQuestion.as_view(), name='data_import'),

# Login urls
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

# Administration pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^ggvadmin/',  include(admin.site.urls)),  # admin site

    
    url(r'^home/$', HomeView.as_view(), name='ggvhome'),
    url(r'^$', IndexView.as_view(), name='splash'),
) 

