from django.urls import path

from screencontrol import views

urlpatterns = [
    path('', views.index, name='home'),
    path('postkeys', views.postkeys, name='post-keys'),
    path('size', views.size, name='video-size'),
    path('video_feed', views.video_feed, name='video-feed'),
]
