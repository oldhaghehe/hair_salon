from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    # Другие пути...
    path('', include('django.contrib.auth.urls')),
]
