from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, ClientProfile


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя с кастомными полями"""

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'role', 'phone', 'birth_date', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['birth_date'].required = True
        self.fields['phone'].required = True


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пользователя с кастомными полями"""

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения пользователей в админ-панели"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username', 'email', 'first_name', 'last_name',
                    'role', 'phone', 'birth_date', 'get_age', 'is_staff', 'is_active')

    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')

    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    ordering = ('-date_joined',)

    list_editable = ('role', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Персональная информация'), {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'address')
        }),
        (_('Права доступа'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',
                       'first_name', 'last_name', 'role', 'phone', 'birth_date', 'address'),
        }),
    )

    def get_age(self, obj):
        """Отображение возраста в списке"""
        return obj.get_age()

    get_age.short_description = 'Возраст'
    get_age.admin_order_field = 'birth_date'


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skin_type', 'allergies_short')
    search_fields = ('user__username', 'user__email')

    def allergies_short(self, obj):
        return obj.allergies[:50] if obj.allergies else '-'

    allergies_short.short_description = 'Аллергии'