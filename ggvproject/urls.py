from django.conf.urls import patterns, include, url
from django.contrib import admin

from filebrowser.sites import site

from utils.wsutil import csvutil, csvutilslides, worksheetvalidator
from core.views import IndexView, HomeView, BookmarkAjaxCreateView, BookmarkAjaxDeleteView, BookmarkAjaxUpdateView
from notes.views import NoteCreateView, NoteView, NoteDeleteView
from courses.views import CourseView
from lessons.views import LessonView, SectionUpdateView
from questions.views import (
    WorksheetHomeView, WorksheetUpdateView, QuestionResponseView,
    OptionQuestionView, OptionQuestionUpdateView,
    TextQuestionView, TextQuestionUpdateView,
    QuestionAssetHandlerView,
    UserReportView, FullReportView
    )
from slidestacks.views import SlideView, SlideAssetHandlerView, SlideStackInfoView, SlideStackUpdateView

urlpatterns = patterns('',

# Utility - NON Production use only!
    url(r'^ggv/utility/$', csvutil, name='util'),
    url(r'^ggv/slideutility/$', csvutilslides, name='slideutil'),
    url(r'^ggv/utility/validator/$', worksheetvalidator.as_view(), name='worksheet_utility'),

# GGV
    url(r'^ggv/(?P<crs_slug>[-\w]+)/$', CourseView.as_view(), name='course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/lesson/(?P<pk>\d+)$', LessonView.as_view(), name='lesson'),

# GGV lesson activities
    # slides are independent files but protected here.
    url(r'^ggv/slidestack/(?P<pk>\d+)/$', SlideStackInfoView.as_view(), name='slide_info_view'),
    url(r'^ggv/slidestack/edit/(?P<pk>\d+)/$', SlideStackUpdateView.as_view(), name='slide_update'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<slideroot>[-\w]+)/$', SlideView.as_view(), name='slideview'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<slideroot>[-\w]+)/data/(?P<asset>.+)/$', SlideAssetHandlerView.as_view(), name='slide_asset'),

    # url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<i>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<i>\d+)/(?P<j>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/report/$', UserReportView.as_view(), name='worksheet_user_report'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/fullreport/$', FullReportView.as_view(), name='worksheet_report'),

    url(r'^ggv/worksheet/(?P<pk>\d+)/$', WorksheetHomeView.as_view(), name='worksheet'),
    url(r'^ggv/worksheet/edit/(?P<pk>\d+)/$', WorksheetUpdateView.as_view(), name='worksheet_update'),

    # url(r'^ggv/section/(?P<pk>\d+)/$', SectionView.as_view(), name='worksheet'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/section/edit/(?P<pk>\d+)/$', SectionUpdateView.as_view(), name='section_update'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/questions/textquestions/(?P<pk>\d+)/$', TextQuestionView.as_view(), name='text_question'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/questions/textquestions/edit/(?P<pk>\d+)/$', TextQuestionUpdateView.as_view(), name='text_question_update'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/questions/optionquestions/(?P<pk>\d+)/$', OptionQuestionView.as_view(), name='option_question'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/questions/optionquestions/edit/(?P<pk>\d+)/$', OptionQuestionUpdateView.as_view(), name='option_question_update'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/questions/(?P<asset>.+)/$', QuestionAssetHandlerView.as_view(), name='question_asset'),


# GGV components
    url(r'^ggv/(?P<crs_slug>[-\w]+)/note/(?P<pk>\d+)/$', NoteView.as_view(), name='view_note'),
    url(r'^ggv/note/add/$', NoteCreateView.as_view(), name='create_note'),
    # url(r'^ggv/note/update/(?P<pk>\d+)/$', NoteUpdateView.as_view(), name='update_note'),
    url(r'^ggv/note/delete/(?P<pk>\d+)/$', NoteDeleteView.as_view(), name='delete_note'),

    url(r'^ggv/bookmark/add/$', BookmarkAjaxCreateView.as_view(), name='create_bookmark'),
    url(r'^ggv/bookmark/update/(?P<pk>\d+)/$', BookmarkAjaxUpdateView.as_view(), name='update_bookmark'),
    url(r'^ggv/bookmark/delete/(?P<pk>\d+)/$', BookmarkAjaxDeleteView.as_view(), name='delete_bookmark'),

# Login urls
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

# Administration pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^ggvadmin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^ggvadmin/',  include(admin.site.urls)),  # admin site


    url(r'^home/$', HomeView.as_view(), name='ggvhome'),
    url(r'^$', IndexView.as_view(), name='splash'),
)

