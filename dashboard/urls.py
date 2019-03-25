from django.urls import path, re_path
from dashboard import views


urlpatterns = [
    path('', views.HomePageView, name='dashboard'),
    re_path(r'^main/(?P<pid>\d+)/$', views.MainView, name='main'),
    path('sentiment', views.SentimentView, name='sentiment'),
    path('crisis', views.CrisisPageView, name='crisis'),
    path('intent', views.IntentPageView, name='intent'),
    path('guard', views.GuardPageView, name='guard'),
    path('reputation', views.ReputationView, name='reputation'),
    path('finance', views.FinanceView, name='finance'),
    path('arabizi', views.ArabiziView, name='arabizi'),
    path('entity', views.EntityView, name='entity'),
    path('topic', views.TopicView, name='topic'),
    re_path(r'^delete-project/(?P<pid>\d+)/$', views.DeleteProject, name='delete-project'),
    path('create-project', views.CreateProject, name='create-project'),
    path('filter/results', views.FilterView, name='filter-view'),
    path('usertoken', views.UserTokenView, name='topic'),
    path('twitter-auth', views.twitterAuth, name='twitter_auth'), 			#Authenticate the user views.py -> auth()
    # path('page', PageView.as_view(), name='page'),
    # path('comment', PageView.as_view(), name='comment'),
    # path('comment', CommentView.as_view(), name='comment'),
    # re_path('page/(?P<page_id>\d+)/$', PageDetailView.as_view(), name='page-detail'),
    # re_path('comments/(?P<page_id>\d+)/$', CommentDetailView.as_view(), name='comment-detail'),
    # path('folder', FolderView.as_view(), name='folder'),
    # re_path('folder/(?P<folder_id>\d+)/$', FolderDetailView.as_view(), name='folder-detail'),
]
