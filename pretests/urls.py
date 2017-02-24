# urls.py

from django.conf.urls import include, url

from .views import PretestHomeView, PretestMenuView, PretestEndView, PretestLogoutView, PretestWorksheetLaunchView, PretestQuestionResponseView

app_name = 'pretests'

urlpatterns = [
	url(r'^$', PretestHomeView.as_view(), name='pretest_home'),
	url(r'^start/$', PretestMenuView.as_view(), name='pretest_menu'),
	url(r'^(?P<pk>\d+)/$', PretestWorksheetLaunchView.as_view(), name='pretest_start'),
	url(r'^(?P<p>\d+)/(?P<q>\d+)/$', PretestQuestionResponseView.as_view(), name='pretest_take'),
	url(r'^done/(?P<pk>\d+)/(?P<user>\d+)$', PretestEndView.as_view(), name='pretest_done'),
	url(r'^logout/$', PretestLogoutView.as_view(), name='pretest_logout'),
	]