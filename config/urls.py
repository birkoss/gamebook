from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from gamebook import views as gamebook_views

urlpatterns = [
    path('', gamebook_views.home, name='home'),

    path('login/', gamebook_views.user_login, name='login'),
    path('logout/', gamebook_views.user_logout, name='logout'),

    path('stories/add/', gamebook_views.edit_story, name='story/add'),
    path('stories/', gamebook_views.story_archive, name='story/archive'),
    path('stories/edit/<str:story_id>/', gamebook_views.edit_story, name='story/edit'),
    path('stories/activate/<str:story_id>/', gamebook_views.edit_story, name='story/activate'),


    path('pages/<str:story_id>/add/', gamebook_views.edit_page, name='page/add'),
    path('pages/<str:story_id>/edit/<str:page_id>/', gamebook_views.edit_page, name='page/edit'),
    path('pages/<str:story_id>/', gamebook_views.page_archive, name='page/archive'),

    path('admin/', admin.site.urls),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
