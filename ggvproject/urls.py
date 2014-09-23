from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from core.views import IndexView, HomeView, NoteCreateView, NoteView
from courses.views import CourseView
from lessons.views import LessonView
from questions.views import WorksheetHomeView, QuestionSetView, QuestionSetResultsView, QuestionResponseView, ImportQuestionDataView
from slidestacks.views import SlideStackInitView, SlideStackView


urlpatterns = patterns('',

# GGV
    url(r'^ggv/(?P<pk>\d+)$', CourseView.as_view(), name='course'),
    url(r'^ggv/lesson/(?P<pk>\d+)$', LessonView.as_view(), name='lesson'),
    
    url(r'^ggv/slidestack-init/(?P<pk>\d+)', SlideStackInitView.as_view(), name='slidestack_init'),
    url(r'^ggv/slidestack/(?P<pk>\d+)', SlideStackView.as_view(), name='slidestack'),
    
    url(r'^ggv/worksheet/(?P<pk>\d+)$', WorksheetHomeView.as_view(), name='worksheet'),
    url(r'^ggv/worksheet/(?P<pk>\d+)/(?P<q>\d+)$', QuestionResponseView.as_view(), name='question'),
    url(r'^ggv/worksheet_results/(?P<pk>\d+)$', QuestionSetResultsView.as_view(), name='worksheet_results'),

    url(r'^ggv/notes/$', NoteView.as_view(), name='list_notes'),
    url(r'^ggv/note/add/$', NoteCreateView.as_view(), name='create_note'),


# Utility - NON Production use only!

    url(r'^ggv/worksheet_import/(?P<pk>\d+)$', ImportQuestionDataView.as_view(), name='data_import'),

# Login urls
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

# Administration pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^ggvadmin/',  include(admin.site.urls)),  # admin site

    
    url(r'^home$', HomeView.as_view(), name='ggvhome'),
    url(r'^$', IndexView.as_view(), name='splash'),
) 

