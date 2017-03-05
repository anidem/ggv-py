# urls.py

from django.conf.urls import include, url

from .views import PretestHomeView, PretestMenuView, PretestEndView, PretestLogoutView, PretestWorksheetLaunchView, PretestQuestionResponseView, PretestLanguageChoiceUpdateView, PretestUserUpdateView, PretestUserListView
from .utils import PretestCreateTokensView, AccessErrorView

app_name = 'pretests'

urlpatterns = [
	url(r'^$', PretestHomeView.as_view(), name='pretest_home'),
	url(r'^access-error/$', AccessErrorView.as_view(), name='pretest_access_error'),
	url(r'^generate-tokens/$', PretestCreateTokensView.as_view(), name='pretest_gen_tokens'),
	url(r'^manage/$', PretestUserListView.as_view(), name='pretest_user_list'),
	url(r'^edit/(?P<pk>\d+)/$', PretestUserUpdateView.as_view(), name='pretest_user_edit'),
	url(r'^start/$', PretestMenuView.as_view(), name='pretest_menu'),
	url(r'^start/language/(?P<pk>\d+)/$', PretestLanguageChoiceUpdateView.as_view(), name='pretest_language_choice'),
	url(r'^(?P<pk>\d+)/$', PretestWorksheetLaunchView.as_view(), name='pretest_start'),
	url(r'^(?P<p>\d+)/(?P<q>\d+)/$', PretestQuestionResponseView.as_view(), name='pretest_take'),
	url(r'^done/(?P<pk>\d+)/(?P<user>\d+)$', PretestEndView.as_view(), name='pretest_done'),
	url(r'^logout/$', PretestLogoutView.as_view(), name='pretest_logout'),
	]