from django import forms
from .models import Appointment, Review, Service


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['master', 'service', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.none()

        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['service'].queryset = Service.objects.filter(masters__id=master_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['service'].queryset = self.instance.master.services.order_by('name')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }
