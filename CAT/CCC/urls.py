from django.urls import path
from . import views

app_name = 'CCC'
urlpatterns = [
    path('', views.MainView, name='main'),
    path('logout', views.LogoutView, name='logout'),
    path('create/', views.CreateJobView, name='create'),
    path('<int:job_id>/', views.DetailView, name='detail'),
    path('<int:job_id>/detail/', views.DetailModalView, name='detailmodal'),
    path('<int:job_id>/abort/', views.AbortView, name='abort'),
    path('<int:job_id>/abort/<int:module_id>/', views.DeleteModuleView, name='deletemodule'),
    path('<int:job_id>/start/', views.ForceStartView, name='start'),
]