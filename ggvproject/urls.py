from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from core.views import IndexView, HomeView
from courses.views import CourseView, StudentCourseView
from lessons.views import LessonView
from questions.views import QuestionSetView
from slidestacks.views import SlideStackView

urlpatterns = patterns('',

# GGV
    url(r'^ggv/(?P<pk>\d+)$', CourseView.as_view(), name='course'),
    url(r'^ggv/lesson/(?P<pk>\d+)$', LessonView.as_view(), name='lesson'),
    url(r'^ggv/slidestack/(?P<pk>\d+)$', SlideStackView.as_view(), name='slidestack'),
    url(r'^ggv/worksheet/(?P<pk>\d+)$', QuestionSetView.as_view(), name='worksheet'),

    # url(r'^ggvstudent/$', StudentAccessView.as_view(), name='student_login'),
    # url(r'^ggvstudent/(?P<pk>\w+)$', StudentCourseView.as_view(), name='course_student'),
    # url(r'^ggvstudent/lesson/(?P<pk>\d+)$', StudentLessonView.as_view(), name='lesson_student'),
    # url(r'^ggvstudent/activity/(?P<pk>\d+)$', StudentActivityView.as_view(), name='activity_student'),

    
# Login urls
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

# Administration pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^ggvadmin/',  include(admin.site.urls)),  # admin site

    url(r'^$', HomeView.as_view(), name='ggvhome'),
)

