from django.contrib import admin

from .models import (Appointment, Master, MasterService, Review, Service)


class MasterServiceInline(admin.TabularInline):
    model = MasterService
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name',)
    inlines = (MasterServiceInline,)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'master', 'service', 'date_time', 'status')
    list_filter = ('status', 'date_time', 'master')
    search_fields = ('client__username', 'master__name', 'service__name')
    readonly_fields = ('total_cost',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'author')
    search_fields = ('author__username', 'appointment__id')
