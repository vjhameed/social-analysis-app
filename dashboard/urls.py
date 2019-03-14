from django.urls import path, re_path
from dashboard.views import HomePageView, CrisisPageView, IntentPageView, GuardPageView, ReputationView, FinanceView, ArabiziView, EntityView, TopicView,SentimentView,DeleteProject,CreateProject,MainView,UserTokenView


urlpatterns = [
    path('', HomePageView, name='dashboard'),
    re_path(r'^main/(?P<pid>\d+)/$', MainView, name='main'),
    path('sentiment', SentimentView, name='sentiment'),
    path('crisis', CrisisPageView, name='crisis'),
    path('intent', IntentPageView, name='intent'),
    path('guard', GuardPageView, name='guard'),
    path('reputation', ReputationView, name='reputation'),
    path('finance', FinanceView, name='finance'),
    path('arabizi', ArabiziView, name='arabizi'),
    path('entity', EntityView, name='entity'),
    path('topic', TopicView, name='topic'),
    re_path(r'^delete-project/(?P<pid>\d+)/$', DeleteProject, name='delete-project'),
    path('create-project', CreateProject, name='create-project'),

    path('usertoken', UserTokenView, name='topic'),
    # path('page', PageView.as_view(), name='page'),
    # path('comment', PageView.as_view(), name='comment'),
    # path('comment', CommentView.as_view(), name='comment'),
    # re_path('page/(?P<page_id>\d+)/$', PageDetailView.as_view(), name='page-detail'),
    # re_path('comments/(?P<page_id>\d+)/$', CommentDetailView.as_view(), name='comment-detail'),
    # path('folder', FolderView.as_view(), name='folder'),
    # re_path('folder/(?P<folder_id>\d+)/$', FolderDetailView.as_view(), name='folder-detail'),
]
