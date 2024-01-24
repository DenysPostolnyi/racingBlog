from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='main-page'),
    path('posts', views.posts, name='posts-page'),
    path('posts/<str:slug>', views.post_detail, name='post-detail-page'),
]