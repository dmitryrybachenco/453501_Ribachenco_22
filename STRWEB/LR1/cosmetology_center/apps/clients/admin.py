from django.contrib import admin
from .models import Appointment, Payment


class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False
    extra = 0


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'doctor', 'service', 'date', 'time', 'status', 'payment_status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('client__first_name', 'client__last_name', 'doctor__user__first_name')
    list_editable = ('status',)
    date_hierarchy = 'date'
    inlines = [PaymentInline]

    def payment_status(self, obj):
        if hasattr(obj, 'payment'):
            return 'Оплачено' if obj.payment.is_paid else 'Не оплачено'
        return 'Не оплачено'

    payment_status.short_description = 'Статус оплаты'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'payment_date', 'is_paid')
    list_filter = ('is_paid', 'payment_date')
    list_editable = ('is_paid',)