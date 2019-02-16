from django.urls import path, re_path
from dashboard.views import SearchSettingView, GeneralDashboardView, BrandDashboard, CompetitiveDashboard, InfluencerDashboard, MentionsDashboard, CreateProject, HomePageView


urlpatterns = [
    path('', HomePageView, name='dashboard'),
    path('brand-dashboard', BrandDashboard, name='brand-dashboard'),
    path('project-setting', SearchSettingView, name='project-setting'),
    path('general-dashboard', GeneralDashboardView, name='searchoutput'),
    path('competitive-dashboard', CompetitiveDashboard, name='comp-dashboard'),
    path('influencer-dashboard', InfluencerDashboard, name='inf-dashboard'),
    path('mentions-dashboard', MentionsDashboard, name='men-dashboard'),
    path('create-project', CreateProject, name='create-project'),
    # path('page', PageView.as_view(), name='page'),
    # path('comment', PageView.as_view(), name='comment'),
    # path('comment', CommentView.as_view(), name='comment'),
    # re_path('page/(?P<page_id>\d+)/$', PageDetailView.as_view(), name='page-detail'),
    # re_path('comments/(?P<page_id>\d+)/$', CommentDetailView.as_view(), name='comment-detail'),
    # path('folder', FolderView.as_view(), name='folder'),
    # re_path('folder/(?P<folder_id>\d+)/$', FolderDetailView.as_view(), name='folder-detail'),
]
