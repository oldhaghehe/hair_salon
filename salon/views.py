from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Service, Master, Appointment, User, Review
from .forms import AppointmentForm, ReviewForm


class LoadServicesView(View):
    def get(self, request, *args, **kwargs):
        master_id = request.GET.get('master_id')
        services = Service.objects.filter(masters__id=master_id).order_by('name')
        return JsonResponse(list(services.values('id', 'name')), safe=False)


class IndexView(TemplateView):
    template_name = 'salon/index.html'



class ServiceListView(ListView):
    model = Service
    template_name = 'salon/services.html'
    context_object_name = 'services'
    paginate_by = 10


class MasterListView(ListView):
    model = Master
    template_name = 'salon/masters.html'
    context_object_name = 'masters'
    paginate_by = 9 # 9 for a 3x3 grid


class MasterDetailView(DetailView):
    model = Master
    template_name = 'salon/master_detail.html'
    context_object_name = 'master'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'salon/appointment_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        response = super().form_valid(form)
        appointment = self.object

        # Send email
        html_message = render_to_string(
            'emails/appointment_created.txt',
            {'user': self.request.user, 'appointment': appointment}
        )
        send_mail(
            'Подтверждение записи в Hair Salon',
            html_message,
            'noreply@hairsalon.com',
            [self.request.user.email],
            fail_silently=False,
        )
        return response

    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'salon/appointment_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})

    def test_func(self):
        return self.get_object().client == self.request.user


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    template_name = 'salon/appointment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})

    def test_func(self):
        return self.get_object().client == self.request.user

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        html_message = render_to_string(
            'emails/appointment_cancelled.txt',
            {'user': request.user, 'appointment': appointment}
        )
        send_mail(
            'Отмена записи в Hair Salon',
            html_message,
            'noreply@hairsalon.com',
            [request.user.email],
            fail_silently=False,
        )
        return super().delete(request, *args, **kwargs)


class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'salon/review_form.html'

    def get_appointment(self):
        return get_object_or_404(Appointment, pk=self.kwargs.get('appointment_id'))

    def test_func(self):
        appointment = self.get_appointment()
        return appointment.client == self.request.user and appointment.status == 'CO'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.appointment = self.get_appointment()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'salon/review_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'salon/review_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('salon:profile', kwargs={'slug': self.request.user.username})


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'salon/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.filter(client=self.object).select_related('master', 'service').prefetch_related('review')
        paginator = Paginator(appointments, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
