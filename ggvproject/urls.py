from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from filebrowser.sites import site

from utils.wsutil import csvutil, csvutilslides, worksheetvalidator
from core.views import (
    IndexView, HomeView,
    BookmarkAjaxCreateView, BookmarkAjaxDeleteView, BookmarkAjaxUpdateView,
    AccessForbiddenView, ActivateView,
    CreateGgvUserView, ListGgvUserView, GgvUserView, UpdateGgvUserView, GgvUserActivationView,
    SendEmailMessageView, FaqView
    )
from notes.views import NoteCreateView, NoteView, NoteDeleteView
from courses.views import CourseView, CourseUpdateView, CourseManageView, UserManageView, UserProgressView, CourseMessageAddView, CourseMessageUpdateView, CourseMessageDeleteView
from lessons.views import LessonView, SectionUpdateView
from questions.views import (
    WorksheetHomeView, WorksheetUpdateView, WorksheetLaunchView, QuestionResponseView,
    OptionQuestionView, OptionQuestionUpdateView,
    TextQuestionView, TextQuestionUpdateView,
    QuestionAssetHandlerView,
    UserReportView, FullReportView,
    LessonKeyView, WorksheetKeyView, WorksheetCompletedView, RestrictResultsUpdateView, TestDocView
    )
from slidestacks.views import SlideView, SlideAssetHandlerView, SlideStackInfoView, SlideStackUpdateView, slide_view

urlpatterns = patterns('',

    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    # url('', include('social.apps.django_app.urls', namespace='disconnect_individual')),
    url(r'^ggv/test/$', TestDocView.as_view(), name='util'),
    url(r'^ggv/emailus/$', SendEmailMessageView.as_view(), name='send_email'),


# Utility - NON Production use only!
    url(r'^ggv/utility/$', csvutil, name='util'),
    url(r'^ggv/slideutility/$', csvutilslides, name='slideutil'),
    url(r'^ggv/utility/validator/$', worksheetvalidator.as_view(), name='worksheet_utility'),

# GGV
    url(r'^ggv/(?P<crs_slug>[-\w]+)/$', CourseView.as_view(), name='course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/edit/$', CourseUpdateView.as_view(), name='edit_course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/manage/$', CourseManageView.as_view(), name='manage_course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/manage/user/(?P<user>\d+)/$', UserManageView.as_view(), name='manage_user'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/progress/user/(?P<user>\d+)/$', UserProgressView.as_view(), name='user_progress'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/lesson/(?P<pk>\d+)/$', LessonView.as_view(), name='lesson'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/lesson/(?P<pk>\d+)/key/$', LessonKeyView.as_view(), name='lesson_key'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/add/message$', CourseMessageAddView.as_view(), name='add_course_msg'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/edit/message/(?P<pk>\d+)/$', CourseMessageUpdateView.as_view(), name='edit_course_msg'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/remove/message/(?P<pk>\d+)/$', CourseMessageDeleteView.as_view(), name='delete_course_msg'),

# GGV lesson activities
    # slides are independent files but protected here.
    url(r'^ggv/slidestack/(?P<pk>\d+)/$', SlideStackInfoView.as_view(), name='slide_info_view'),
    url(r'^ggv/slidestack/edit/(?P<pk>\d+)/$', SlideStackUpdateView.as_view(), name='slide_update'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<pk>[-\w]+)/$', slide_view.as_view(), name='slideview'),
    # url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<slideroot>[-\w]+)/$', 'slidestacks.views.slide_view', name='slideview'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<slideroot>[-\w]+)/data/(?P<asset>.+)/$', SlideAssetHandlerView.as_view(), name='slide_asset'),

    # url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<i>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/$', WorksheetLaunchView.as_view(), name='worksheet_launch'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<i>\d+)/(?P<j>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/report/(?P<user>\d+)/$', UserReportView.as_view(), name='worksheet_user_report'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/fullreport/$', FullReportView.as_view(), name='worksheet_report'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/key/$', WorksheetKeyView.as_view(), name='worksheet_key'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/status-update/(?P<pk>\d+)/$', RestrictResultsUpdateView.as_view(), name='worksheet_report_access'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet-completed/(?P<pk>\d+)/$', WorksheetCompletedView.as_view(), name='worksheet_completed'),



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


# Users
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/add/$', CreateGgvUserView.as_view(), name='create_user'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/list/$', ListGgvUserView.as_view(), name='list_users'),
    url(r'^ggv/user/(?P<pk>[-\d]+)/$', GgvUserView.as_view(), name='view_user'),
    url(r'^ggv/user/edit/(?P<pk>[-\d]+)/', UpdateGgvUserView.as_view(), name='edit_user'),
    url(r'^ggv/user/deactivate/(?P<pk>[-\d]+)/$', GgvUserActivationView.as_view(), name='update_user_activation'),

# Login urls

    url(r'^login/$', include('social.apps.django_app.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^clean-logout/$', 'core.utils.logout_clean', name='logout_clean'),

    # url(r'^activate/$', ActivateView.as_view(), name='activate'),
    # url(r'^activate/(?P<backend>[^/]+)/$', ActivateView.as_view(), name='activate'),

    url(r'^access-forbidden/$', AccessForbiddenView.as_view(), name='access_forbidden'),

# Administration pages

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^ggvadmin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^ggvadmin',  include(admin.site.urls)),  # admin site


    url(r'^faq/$', FaqView.as_view(), name='faq'),
    url(r'^home/$', HomeView.as_view(), name='ggvhome'),
    url(r'^', IndexView.as_view(), name='splash'),
)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


