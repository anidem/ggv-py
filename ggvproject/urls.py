from django.conf.urls import include, url
from django.conf.urls.static import static
# from django.conf.urls.defaults import handler500, handler404
from django.contrib import admin
from django.contrib.auth import views
from django.conf import settings

from filebrowser.sites import site

from ggvutils.wsutil import csvutil, csvutilslides, worksheetvalidator

from core.emails import (
    SendEmailWorksheetQuestionToInstructorsView, 
    SendEmailWorksheetErrorToStaffView, 
    SendEmailToStaff, 
    SendEmailToInstructor,
    SendEmailToManagerDeactivationRequest,
    SendEmailToManagerActivationRequest,
    SendEmailToAllActiveUsers,
    SendEmailToGgvOrgUsers,
    SendEmailToCourseUsers
    )
from core.utils import logout_clean
from core.views import (
    IndexView, HomeView,
    BookmarkAjaxCreateView, BookmarkAjaxDeleteView, BookmarkAjaxUpdateView,
    AccessForbiddenView,
    CreateGgvUserView, UpdateGgvUserAccountView,  GgvUserView, UpdateGgvUserView, CreateGgvUserAccountRequestView, UpdateGgvUserAccountRequestView, DeleteGgvUserAccountRequestView, GgvUserActivationView, GgvUserArchiveThenDeleteView, GgvUserDeleteUnusedAccount,
    PolicyView, FaqView, GgvUsersDeactivationView, GgvUsersActivationView, AttendanceAjaxCodeUpdateView, AttendanceAjaxCodeCreateView, AttendanceAjaxCodeDeleteView, AttendanceUpdateAllView,
    HelpView, HelpCreateView, HelpUpdateView, HelpListView,
    )
from notes.views import NoteCreateView, NoteView, NoteDeleteView
from courses.views import (
    GgvOrgAdminView, GgvOrgUserActivityReportView,
    CourseView, CourseUpdateView, CourseGraderEditView, CourseGraderCreateView, CourseGraderDeleteView, CourseManageView, CourseUserReportView, CourseUserActivityReportView, CourseUserActivityFullReportView, CourseGraderLogView,
    CourseAttendanceMonthView, CourseAttendanceUserView,
    UserManageView, UserProgressView, UserProgressViewDateSelector,
    CourseMessageAddView, CourseMessageUpdateView, CourseMessageDeleteView
    )
from lessons.views import LessonView, SectionUpdateView
from questions.views import (
    WorksheetHomeView, WorksheetUpdateView, WorksheetLaunchView, QuestionResponseView,
    OptionQuestionView, OptionQuestionUpdateView,
    TextQuestionView, TextQuestionUpdateView,
    QuestionAssetHandlerView,
    UserReportView, FullReportView, UserResponsesResetView, QuestionResponseGradeView,
    LessonKeyView, WorksheetKeyView, WorksheetCompletedView, RestrictResultsUpdateView, TestDocView
    )
from slidestacks.views import SlideView, SlideAssetHandlerView, SlideStackInfoView, SlideStackUpdateView, slide_view
from supportmedia.views import ExternalMediaView, ExternalMediaCourseView, ExternalMediaCreateView, ExternalMediaUpdateView
from pretests.views import PretestHomeView

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'session_security/', include('session_security.urls')),
    
    url(r'^pretest/', include('pretests.urls', namespace='pretestapp')),


    url(r'^ggv/test/$', TestDocView.as_view(), name='util'),
    url(r'^ggv/email-us/$', SendEmailToStaff.as_view(), name='email_staff'),

# Utility - NON Production use only!
    url(r'^ggv/utility/$', csvutil, name='util'),
    url(r'^ggv/slideutility/$', csvutilslides, name='slideutil'),
    # url(r'^ggv/utility/validator/$', worksheetvalidator.as_view(), name='worksheet_utility'),

    # slides are independent files but protected here.
    url(r'^ggv/slidestack/(?P<pk>\d+)/$', SlideStackInfoView.as_view(), name='slide_info_view'),
    url(r'^ggv/slidestack/edit/(?P<pk>\d+)/$', SlideStackUpdateView.as_view(), name='slide_update'),

# AttendanceUpdateAllView
    url(r'^ggv/update-attendance/$', AttendanceUpdateAllView.as_view(), name='update_attendance_all'),

# GGV Organizations
    url(r'^ggv/organization/(?P<pk>\d+)/$', GgvOrgAdminView.as_view(), name='manage_org'),
    url(r'^ggv/organization/(?P<pk>\d+)/activity-report/$', GgvOrgUserActivityReportView.as_view(), name='report_org_activity'),
    url(r'^ggv/organization/(?P<pk>\d+)/email-users/$', SendEmailToGgvOrgUsers.as_view(), name='email_org_users'),

# GGV Courses
    url(r'^ggv/(?P<crs_slug>[-\w]+)/$', CourseView.as_view(), name='course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/edit/$', CourseUpdateView.as_view(), name='edit_course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/grader/add/$', CourseGraderCreateView.as_view(), name='add_course_grader'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/grader/edit/(?P<pk>\d+)/$', CourseGraderEditView.as_view(), name='edit_course_grader'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/grader/delete/(?P<pk>\d+)/$', CourseGraderDeleteView.as_view(), name='delete_course_grader'),
    url(r'^ggv/grader/log/$', CourseGraderLogView.as_view(), name='course_grader_log'),

    #  course user stats:
    url(r'^ggv/(?P<crs_slug>[-\w]+)/report/$', CourseUserReportView.as_view(), name='report_course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/activity-report/$', CourseUserActivityReportView.as_view(), name='report_course_activity'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/full-activity-report/$', CourseUserActivityFullReportView.as_view(), name='report_full_course_activity'),


    url(r'^ggv/(?P<crs_slug>[-\w]+)/manage/$', CourseManageView.as_view(), name='manage_course'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/manage/user/(?P<user>\d+)/$', UserManageView.as_view(), name='manage_user'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/progress/user/(?P<user>\d+)/$', UserProgressView.as_view(), name='user_progress'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/progress/user/custom/(?P<user>\d+)/$', UserProgressViewDateSelector.as_view(), name='user_progress_custom'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/attendance/update/(?P<pk>\d+)/$', AttendanceAjaxCodeUpdateView.as_view(), name='course_attendance_update'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/attendance/delete/(?P<pk>\d+)/$', AttendanceAjaxCodeDeleteView.as_view(), name='course_attendance_delete'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/attendance/add/(?P<user>\d+)/$', AttendanceAjaxCodeCreateView.as_view(), name='course_attendance_add'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/attendance/user/(?P<user>\d+)/$', CourseAttendanceUserView.as_view(), name='course_attendance_user'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/attendance/current/$', CourseAttendanceMonthView.as_view(), name='course_attendance_current'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/attendance/(?P<year>\d+)/(?P<month>\d+)/$', CourseAttendanceMonthView.as_view(), name='course_attendance_selected'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/email-users/$', SendEmailToCourseUsers.as_view(), name='email_course_users'),



    url(r'^ggv/(?P<crs_slug>[-\w]+)/lesson/(?P<pk>\d+)/$', LessonView.as_view(), name='lesson'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/lesson/(?P<pk>\d+)/key/$', LessonKeyView.as_view(), name='lesson_key'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/add/message/$', CourseMessageAddView.as_view(), name='add_course_msg'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/edit/message/(?P<pk>\d+)/$', CourseMessageUpdateView.as_view(), name='edit_course_msg'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/remove/message/(?P<pk>\d+)/$', CourseMessageDeleteView.as_view(), name='delete_course_msg'),

# GGV lesson activities

    url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<pk>[-\w]+)/$', slide_view.as_view(), name='slideview'),
    # url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<slideroot>[-\w]+)/$', 'slidestacks.views.slide_view', name='slideview'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/slidestack/(?P<slideroot>[-\w]+)/data/(?P<asset>.+)/$', SlideAssetHandlerView.as_view(), name='slide_asset'),

    # url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<i>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/$', WorksheetLaunchView.as_view(), name='worksheet_launch'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<i>\d+)/(?P<j>\d+)/$', QuestionResponseView.as_view(), name='question_response'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/report/(?P<user>\d+)/$', UserReportView.as_view(), name='worksheet_user_report'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/worksheet/(?P<pk>\d+)/reset/(?P<user>\d+)/$', UserResponsesResetView.as_view(), name='reset_worksheet_responses'),
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

    url(r'^ggv/support-media/external-media/(?P<pk>\d+)/$', ExternalMediaView.as_view(), name='external_media_view'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/support-media/external-media/(?P<pk>\d+)/$', ExternalMediaCourseView.as_view(), name='external_media_view_crs'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/support-media/external-media/add/$', ExternalMediaCreateView.as_view(), name='external_media_add'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/support-media/external-media/edit/(?P<pk>\d+)/$', ExternalMediaUpdateView.as_view(), name='external_media_update'),

    url(r'^ggv/grade/(?P<pk>\d+)/$', QuestionResponseGradeView.as_view(), name='question_response_grade'),



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
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/(?P<pk>[-\d]+)/$', GgvUserView.as_view(), name='view_user'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/edit-account/(?P<pk>[-\d]+)/$', UpdateGgvUserAccountView.as_view(), name='edit_user_account'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/edit/(?P<pk>[-\d]+)/$', UpdateGgvUserView.as_view(), name='edit_user'),
    
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/request/$', CreateGgvUserAccountRequestView.as_view(), name='request_user_account'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/request/edit/(?P<pk>[-\d]+)/$', UpdateGgvUserAccountRequestView.as_view(), name='edit_request_user_account'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/user/request/delete/(?P<pk>[-\d]+)/$', DeleteGgvUserAccountRequestView.as_view(), name='delete_request_user_account'),

    url(r'^ggv/user/deactivate/(?P<pk>[-\d]+)/$', GgvUserActivationView.as_view(), name='update_user_activation'),
    url(r'^ggv/users/deactivate/$', GgvUsersDeactivationView.as_view(), name='deactivate_users'),
    url(r'^ggv/users/activate/$', GgvUsersActivationView.as_view(), name='activate_users'),
    url(r'^ggv/users/delete-unused/$', GgvUserDeleteUnusedAccount.as_view(), name='delete_unused_user'),
    url(r'^ggv/users/archive-delete/$', GgvUserArchiveThenDeleteView.as_view(), name='archive_delete_user'),
    # deprecate => url(r'^ggv/(?P<crs_slug>[-\w]+)/user/list/$', ListGgvUserView.as_view(), name='list_users'),

    # Login urls

    url(r'^login/', include('social.apps.django_app.urls')),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^clean-logout/$', logout_clean, name='logout_clean'),

    # url(r'^activate/$', ActivateView.as_view(), name='activate'),
    # url(r'^activate/(?P<backend>[^/]+)/$', ActivateView.as_view(), name='activate'),

    url(r'^access-forbidden/$', AccessForbiddenView.as_view(), name='access_forbidden'),

# Email handling
    url(r'^ggv/(?P<crs_slug>[-\w]+)/email-question/worksheet/(?P<i>\d+)/(?P<j>\d+)/$', SendEmailWorksheetQuestionToInstructorsView.as_view(), name='email_instructor_question'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/email-error/worksheet/(?P<i>\d+)/(?P<j>\d+)/$', SendEmailWorksheetErrorToStaffView.as_view(), name='email_staff_ws_error'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/email-instructor/$', SendEmailToInstructor.as_view(), name='email_instructor'),

    url(r'^ggv/(?P<crs_slug>[-\w]+)/email-manager/deactivate$', SendEmailToManagerDeactivationRequest.as_view(), name='email_manager_deactivate'),
    url(r'^ggv/(?P<crs_slug>[-\w]+)/email-manager/activate$', SendEmailToManagerActivationRequest.as_view(), name='email_manager_activate'), 

    url(r'^ggv/system/email-system-users/$', SendEmailToAllActiveUsers.as_view(), name='email_system_users'),

# Administration pages

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^ggvadmin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^ggvadmin/',  admin.site.urls, name='staff_admin'),  # admin site

    url(r'^help/add/$', HelpCreateView.as_view(), name='help_page_create'),
    url(r'^help/edit/(?P<slug>[-\w]+)/$', HelpUpdateView.as_view(), name='help_page_edit'),
    url(r'^help/list/$', HelpListView.as_view(), name='help_page_list'),
    url(r'^help/(?P<slug>[-\w]+)/$', HelpView.as_view(), name='help_page'),



    url(r'^faq/$', FaqView.as_view(), name='faq'),
    url(r'^policy/$', PolicyView.as_view(), name='policy'),
    url(r'^home/$', HomeView.as_view(), name='ggvhome'),
    url(r'^', IndexView.as_view(), name='splash'),
 
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
