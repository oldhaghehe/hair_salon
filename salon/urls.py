from django.urls import path

from . import views

app_name = 'salon'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('masters/', views.MasterListView.as_view(), name='masters'),
    path('masters/<int:pk>/', views.MasterDetailView.as_view(), name='master_detail'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointment/<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointment/<int:appointment_id>/review/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_edit'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
    path('ajax/load-services/', views.load_services, name='ajax_load_services'),
]
