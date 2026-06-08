from django.contrib import admin
from .models import Review, PromoCode, Coupon


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'text_short', 'created_at', 'is_moderated')
    list_filter = ('rating', 'is_moderated', 'created_at')
    search_fields = ('user__username', 'user__email', 'text')
    list_editable = ('is_moderated',)
    list_display_links = ('user',)
    readonly_fields = ('created_at',)

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Текст'


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active', 'is_valid')
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    list_editable = ('discount_percent', 'is_active')

    def get_valid_status(self, obj):
        """Проверяет, активен ли промокод в данный момент"""
        from django.utils import timezone
        now = timezone.now()
        is_valid = obj.is_active and obj.valid_from <= now <= obj.valid_to
        return 'Да' if is_valid else 'Нет'
    get_valid_status.short_description = 'Действует сейчас'
    get_valid_status.boolean = True


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'discount_amount', 'valid_until', 'is_used', 'user')
    list_filter = ('is_used', 'valid_until')
    search_fields = ('coupon_code', 'user__email')
    list_editable = ('is_used',)