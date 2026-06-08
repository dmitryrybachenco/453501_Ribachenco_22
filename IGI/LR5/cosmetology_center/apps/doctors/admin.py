from django.contrib import admin
from .models import DoctorSpecialization, Doctor, Schedule


@admin.register(DoctorSpecialization)
class DoctorSpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor_count')
    search_fields = ('name',)

    def doctor_count(self, obj):
        return obj.doctors.count()

    doctor_count.short_description = 'Количество врачей'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years', 'services_count')
    list_filter = ('specializations',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('specializations', 'services')

    def services_count(self, obj):
        return obj.services.count()

    services_count.short_description = 'Услуги'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('doctor', 'date', 'is_available')
    list_editable = ('is_available',)
    date_hierarchy = 'date'