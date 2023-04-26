from django.urls import path

from . import views

app_name = 'miniforum'
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('threads/', views.ThreadIndexView.as_view(), name='thread_index'),
    path('threads/create/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('threads/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('threads/<int:pk>/posts', views.PostIndexView.as_view(), name='post_index'),
    path('threads/<int:pk>/posts/create', views.PostCreateView.as_view(), name='post_create'),
    path('threads/<int:pk>/report', views.ReportCreateView.as_view(), name='report_create'),
    path('threads/<int:pk>/report/done', views.ReportDoneView.as_view(), name='report_done'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register')
]
