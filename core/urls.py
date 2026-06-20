from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('team/', views.team, name='team'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
