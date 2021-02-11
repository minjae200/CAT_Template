from django.urls import path
from . import views

app_name = 'CCC'
urlpatterns = [
    path('', views.MainView, name='main'),
    path('create/', views.CreateView, name='create'),
    path('create/register', views.CreateJobView, name='register'),
    path('<int:job_id>/', views.DetailView, name='detail'),
    path('<int:job_id>/abort/', views.AbortView, name='abort'),
    path('<int:job_id>/start/', views.ForceStartView, name='start'),
]