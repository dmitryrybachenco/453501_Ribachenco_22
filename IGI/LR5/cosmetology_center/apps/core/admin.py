from django.contrib import admin
from .models import (
    News, Glossary, Contact, Vacancy,
    CompanyInfo, CompanyHistory, CompanyRequirement
)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    date_hierarchy = 'published_at'
    prepopulated_fields = {'slug': ('title',)} if 'slug' in [f.name for f in News._meta.fields] else {}


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ('term', 'definition_short', 'added_at')
    search_fields = ('term', 'definition')

    def definition_short(self, obj):
        return obj.definition[:50] + '...' if len(obj.definition) > 50 else obj.definition

    definition_short.short_description = 'Определение'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone', 'email', 'order', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('full_name', 'position', 'email')
    list_editable = ('order', 'is_active')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'location', 'created_at')
    search_fields = ('title', 'description', 'requirements')
    list_editable = ('is_active',)


class CompanyHistoryInline(admin.TabularInline):
    model = CompanyHistory
    extra = 1


class CompanyRequirementInline(admin.TabularInline):
    model = CompanyRequirement
    extra = 1


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'inn')
    fieldsets = (
        ('Основная информация', {
            'fields': ('company_name', 'short_description', 'full_description', 'logo', 'video_url')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email', 'legal_address', 'actual_address')
        }),
        ('Реквизиты', {
            'fields': ('inn', 'ogrn', 'bank_details')
        }),
    )
    inlines = [CompanyHistoryInline, CompanyRequirementInline]


@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'event')
    list_filter = ('company', 'year')
    search_fields = ('event',)


@admin.register(CompanyRequirement)
class CompanyRequirementAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'value')
    list_filter = ('company',)