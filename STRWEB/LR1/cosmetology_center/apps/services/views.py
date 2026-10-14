from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Service, ServiceCategory


def service_list(request):
    """Список всех услуг"""
    services = Service.objects.filter(is_active=True).select_related('category')
    categories = ServiceCategory.objects.annotate(
        service_count=Count('services', filter=Q(services__is_active=True))
    ).filter(service_count__gt=0)

    category_id = request.GET.get('category')
    if category_id:
        services = services.filter(category_id=category_id)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)

    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        services = services.order_by('price')
    elif sort_by == 'price_desc':
        services = services.order_by('-price')
    elif sort_by == 'name_asc':
        services = services.order_by('name')
    else:
        services = services.order_by('category', 'name')

    query = request.GET.get('q')
    if query:
        services = services.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'query': query,
    }
    return render(request, 'services/service_list.html', context)


def service_detail(request, pk):
    """Детальная страница услуги"""
    service = get_object_or_404(Service, pk=pk, is_active=True)

    doctors = service.doctors.all().select_related('user')[:5]

    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(pk=pk)[:4]

    context = {
        'service': service,
        'doctors': doctors,
        'related_services': related_services,
    }
    return render(request, 'services/service_detail.html', context)


def service_category_detail(request, pk):
    """Детальная страница категории услуг"""
    category = get_object_or_404(ServiceCategory, pk=pk)
    services = Service.objects.filter(category=category, is_active=True)

    context = {
        'category': category,
        'services': services,
    }
    return render(request, 'services/category_detail.html', context)