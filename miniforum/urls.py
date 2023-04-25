from django.urls import path

from . import views

app_name = 'miniforum'
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('threads/', views.ThreadIndexView.as_view(), name='thread_index'),
    path('threads/create/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('threads/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('threads/<int:pk>/post', views.PostCreateView.as_view(), name='post_create'),
]
