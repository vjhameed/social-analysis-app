from django.urls import path, re_path
from accounts import views as account_views

urlpatterns = [
    path('login/', account_views.ManualLoginView.as_view(), name='login'),
    path('signup/', account_views.SignUpView.as_view(), name='signup'),
    # path('dashboard/', account_views.DashboardView.as_view(), name='dashboard'),
    path('reset/', account_views.ResetView.as_view(), name='reset'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account_views.reset_confirm, name='password_reset_confirm'),
    path('change/password', account_views.ChangePasswordView.as_view(), name='change-password'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account_views.activate, name='activate'),
    path('logout/', account_views.Logout, name='logout'),
]
