# urls.py

from django.conf.urls import include, url

from .views import PretestHomeView, PretestMenuView, PretestEndView, PretestLogoutView, PretestWorksheetLaunchView, PretestQuestionResponseView, PretestLanguageChoiceUpdateView, PretestUserCreateView, PretestUserUpdateView, PretestUserUpdateFromGoogleView, PretestUserCreateFromGoogleView, PretestUserListView, PretestAccountListView, PretestUserDetailView, PretestEndConfirmView, PretestAccountReportView, PretestAccountReportProtectedView, PretestResponseGradeView, PretestToggleFlagView, PretestCreateGgvUserAccountRequestView
from .utils import PretestCreateTokensView, AccessErrorView
from .emails import SendPretestTokenView
app_name = 'pretests'

urlpatterns = [
	url(r'^$', PretestHomeView.as_view(), name='pretest_home'),
	url(r'^access/(?P<token>[\w!#@]+)/$', PretestHomeView.as_view(), name='pretest_home_shortcut'),
	url(r'^access-error/$', AccessErrorView.as_view(), name='pretest_access_error'),
	url(r'^generate-tokens/$', PretestCreateTokensView.as_view(), name='pretest_gen_tokens'),
	url(r'^accounts/$', PretestAccountListView.as_view(), name='pretest_account_list'),
	url(r'^manage/(?P<pk>\d+)/$', PretestUserListView.as_view(), name='pretest_user_list'),
	url(r'^view/(?P<pk>\d+)/$', PretestUserDetailView.as_view(), name='pretest_user_detail'),
	
	url(r'^add/(?P<account>\d+)/$', PretestUserCreateView.as_view(), name='pretest_user_add'),
	url(r'^add-google/(?P<account>\d+)/$', PretestUserCreateFromGoogleView.as_view(), name='pretest_user_add_from_google'),
	
	url(r'^edit/(?P<pk>\d+)/$', PretestUserUpdateView.as_view(), name='pretest_user_edit'),	
	url(r'^edit-google/(?P<pk>\d+)/$', PretestUserUpdateFromGoogleView.as_view(), name='pretest_user_edit_from_google'),

	url(r'^ggvuser/request/(?P<account>\d+)/(?P<pretest_user_account>\d+)/$', PretestCreateGgvUserAccountRequestView.as_view(), name='pretest_request_user_account'),
	
	url(r'^email/(?P<pk>\d+)/$', SendPretestTokenView.as_view(), name='pretest_send_token'),
	url(r'^start/$', PretestMenuView.as_view(), name='pretest_menu'),
	url(r'^start/language/(?P<pk>\d+)/$', PretestLanguageChoiceUpdateView.as_view(), name='pretest_language_choice'),
	url(r'^(?P<pk>\d+)/$', PretestWorksheetLaunchView.as_view(), name='pretest_start'),
	url(r'^(?P<p>\d+)/(?P<q>\d+)/$', PretestQuestionResponseView.as_view(), name='pretest_take'),
	url(r'^done/confirm/(?P<pk>\d+)/$', PretestEndConfirmView.as_view(), name='pretest_confirm_done'),
	url(r'^done/(?P<pk>\d+)/(?P<user>\d+)/$', PretestEndView.as_view(), name='pretest_done'),
	url(r'^logout/$', PretestLogoutView.as_view(), name='pretest_logout'),
	url(r'^grade/(?P<pk>\d+)/$', PretestResponseGradeView.as_view(), name='pretest_response_grade'),
	url(r'^troper/(?P<pk>\d+)/$', PretestAccountReportView.as_view(), name='pretest_account_report'),
	url(r'^staff-report/(?P<pk>\d+)/$', PretestAccountReportProtectedView.as_view(), name='pretest_account_staff_report'),
	url(r'^flag/$', PretestToggleFlagView.as_view(), name='pretest_flagger'),
	]