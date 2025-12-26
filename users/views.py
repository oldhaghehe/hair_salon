from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserEditForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('salon:index')
    template_name = 'users/signup.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})
