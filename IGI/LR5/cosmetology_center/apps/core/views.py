import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.contrib import messages
from django.utils import timezone
import pytz
from datetime import datetime
from .models import News, Glossary, Contact, Vacancy
from .forms import ReviewForm, NewsForm
from apps.services.models import Service, ServiceCategory
from apps.doctors.models import Doctor
from ..analytics.models import Review, PromoCode

logger = logging.getLogger(__name__)


def get_user_timezone(request):
    """Получение часового пояса пользователя"""
    tz_name = request.session.get('timezone', 'Europe/Minsk')
    return pytz.timezone(tz_name)


def home(request):
    """Главная страница"""
    logger.info(f"User {request.user} accessed home page")

    latest_news = News.objects.filter(is_published=True).order_by('-published_at').first()

    popular_services = Service.objects.filter(is_active=True)[:6]

    top_doctors = Doctor.objects.annotate(
        appointment_count=Count('appointments')
    ).order_by('-appointment_count')[:4]

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'latest_news': latest_news,
        'popular_services': popular_services,
        'top_doctors': top_doctors,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/home.html', context)


def about(request):
    """Страница о компании"""
    logger.info(f"About page accessed by {request.user}")

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'company_history': [
            {'year': 2015, 'event': 'Основание косметологического центра'},
            {'year': 2017, 'event': 'Открытие второго филиала'},
            {'year': 2019, 'event': 'Внедрение лазерных технологий'},
            {'year': 2021, 'event': 'Получение международной аккредитации'},
            {'year': 2024, 'event': 'Запуск онлайн-записи'},
        ],
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/about.html', context)


def news_list(request):
    """Список новостей"""
    news_list = News.objects.filter(is_published=True).order_by('-published_at')

    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'page_obj': page_obj,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/news_list.html', context)


def news_detail(request, pk):
    """Детальная страница новости"""
    news = get_object_or_404(News, pk=pk, is_published=True)

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')
    news_date_utc = news.published_at.strftime('%d/%m/%Y')
    news_date_local = news.published_at.astimezone(user_tz).strftime('%d/%m/%Y')

    context = {
        'news': news,
        'current_date': current_date,
        'news_date_utc': news_date_utc,
        'news_date_local': news_date_local,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/news_detail.html', context)


def glossary(request):
    """Словарь терминов"""
    glossary_items = Glossary.objects.all().order_by('term')

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'glossary_items': glossary_items,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/glossary.html', context)


def contacts(request):
    """Страница контактов"""
    contacts = Contact.objects.filter(is_active=True)

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'contacts': contacts,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/contacts.html', context)


def privacy_policy(request):
    """Политика конфиденциальности"""
    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    return render(request, 'core/privacy.html', {
        'current_date': current_date,
        'user_timezone': str(user_tz),
    })


def vacancies(request):
    """Вакансии"""
    vacancies_list = Vacancy.objects.filter(is_active=True).order_by('-created_at')

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'vacancies': vacancies_list,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/vacancies.html', context)


def reviews(request):
    """Отзывы"""
    reviews_list = Review.objects.filter(is_moderated=True).order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв добавлен и ожидает модерации!')
            return redirect('core:reviews')
    else:
        form = ReviewForm()

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'reviews': reviews_list,
        'form': form,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/reviews.html', context)


@login_required
def create_review(request):
    """Создание отзыва через отдельную страницу"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после модерации.')
            return redirect('core:reviews')
    else:
        form = ReviewForm()

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    return render(request, 'core/create_review.html', {
        'form': form,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    })


def promocodes(request):
    """Промокоды и купоны"""
    active_promocodes = PromoCode.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now()
    )
    archived_promocodes = PromoCode.objects.filter(
        Q(valid_to__lt=timezone.now()) | Q(is_active=False)
    )

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'active_promocodes': active_promocodes,
        'archived_promocodes': archived_promocodes,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/promocodes.html', context)


def search(request):
    """Поиск по сайту"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    sort_by = request.GET.get('sort', '')

    results = {
        'services': [],
        'doctors': [],
        'news': [],
        'vacancies': [],
    }

    if query:
        if search_type in ['all', 'services']:
            results['services'] = Service.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_active=True
            )
            if sort_by == 'price_asc':
                results['services'] = results['services'].order_by('price')
            elif sort_by == 'price_desc':
                results['services'] = results['services'].order_by('-price')
            elif sort_by == 'name_asc':
                results['services'] = results['services'].order_by('name')

        if search_type in ['all', 'doctors']:
            results['doctors'] = Doctor.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(specializations__name__icontains=query)
            ).distinct()

        if search_type in ['all', 'news']:
            results['news'] = News.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                is_published=True
            )
            if sort_by == 'date_desc':
                results['news'] = results['news'].order_by('-published_at')

        if search_type in ['all', 'vacancies']:
            results['vacancies'] = Vacancy.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query),
                is_active=True
            )

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'query': query,
        'search_type': search_type,
        'sort_by': sort_by,
        'results': results,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/search_results.html', context)


@staff_member_required
def news_create(request):
    """Создание новой новости (только для superuser/staff)"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            messages.success(request, f'Новость "{news.title}" успешно создана!')
            return redirect('core:news_detail', pk=news.pk)
    else:
        form = NewsForm()

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'form': form,
        'title': 'Создание новости',
        'button_text': 'Создать',
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/news_form.html', context)


@staff_member_required
def news_edit(request, pk):
    """Редактирование новости (только для superuser/staff)"""
    news = get_object_or_404(News, pk=pk)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, f'Новость "{news.title}" успешно обновлена!')
            return redirect('core:news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'form': form,
        'news': news,
        'title': 'Редактирование новости',
        'button_text': 'Сохранить',
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/news_form.html', context)


@staff_member_required
def news_delete(request, pk):
    """Удаление новости (только для superuser/staff)"""
    news = get_object_or_404(News, pk=pk)

    if request.method == 'POST':
        news_title = news.title
        news.delete()
        messages.success(request, f'Новость "{news_title}" успешно удалена!')
        return redirect('core:news_list')

    user_tz = get_user_timezone(request)
    current_date = datetime.now(user_tz).strftime('%d/%m/%Y')

    context = {
        'news': news,
        'current_date': current_date,
        'user_timezone': str(user_tz),
    }
    return render(request, 'core/news_confirm_delete.html', context)