from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from facebookPages.views import HomePage

urlpatterns = [
    path('', HomePage),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('facebook/', include('facebook.urls')),
    path('dashboard/', include('dashboard.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
