from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from core.views import HomeView, CourseView, StudentCourseView
from questions.views import MultipleChoiceQuestionDetailView, MultipleChoiceQuestionCreateView
from lessons.views  import ( 
    LessonView,
    ActivityView,
    StudentLessonView,
    StudentAccessView,
    StudentActivityView,
    )

urlpatterns = patterns('',
    url(r'^mc/(?P<pk>\d+)$', MultipleChoiceQuestionDetailView.as_view(), name='multiplechoice'),
    url(r'^mc/new$', MultipleChoiceQuestionCreateView.as_view(), name='newmc'),

    url(r'^ggv/$', HomeView.as_view(), name='ggvhome'),
    url(r'^ggv/(?P<pk>\d+)$', CourseView.as_view(), name='course'),
    url(r'^ggv/lesson/(?P<pk>\d+)$', LessonView.as_view(), name='lesson'),
    url(r'^ggv/activity/(?P<pk>\d+)$', ActivityView.as_view(), name='activity'),

    url(r'^ggvstudent/$', StudentAccessView.as_view(), name='student_login'),
    url(r'^ggvstudent/(?P<pk>\w+)$', StudentCourseView.as_view(), name='course_student'),
    url(r'^ggvstudent/lesson/(?P<pk>\d+)$', StudentLessonView.as_view(), name='lesson_student'),
    url(r'^ggvstudent/activity/(?P<pk>\d+)$', StudentActivityView.as_view(), name='activity_student'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^admin/', include(admin.site.urls)),
)
