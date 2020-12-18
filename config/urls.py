from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from gamebook import views as gamebook_views

urlpatterns = [
    path('', gamebook_views.home, name='home'),
    path('login/', gamebook_views.user_login, name='login'),
    path('logout/', gamebook_views.user_logout, name='logout'),
    path('admin/', admin.site.urls),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
