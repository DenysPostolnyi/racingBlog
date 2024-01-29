from django.urls import path

from blog import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='main-page'),
    path('posts', views.AllPostsView.as_view(), name='posts-page'),
    path('posts/<str:slug>', views.SinglePostView.as_view(), name='post-detail-page'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later'),
    path('stored-posts', views.ReadLaterView.as_view(), name='stored-posts-page'),
]
