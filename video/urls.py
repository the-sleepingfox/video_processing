from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name= 'upload_video'),
    path('videos/', views.video_list, name= 'video_list'),
    path('videos/<int:video_id>/', views.video_detail, name= 'video_detail'),
    path('delete_video/<str:video_id>',views.delete_video, name='delete_video'),
    path('search/', views.search_subtitle, name='search_subtitle'),
]
