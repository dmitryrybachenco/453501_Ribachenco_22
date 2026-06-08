from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import User
from apps.clients.models import Appointment


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.get_full_name()}!')
            return redirect('core:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'С возвращением, {user.get_full_name()}!')

            next_url = request.GET.get('next', 'core:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('core:home')


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    recent_appointments = Appointment.objects.filter(
        client=request.user
    ).select_related('doctor', 'service').order_by('-date', '-time')[:5]

    context = {
        'user': request.user,
        'recent_appointments': recent_appointments,
    }

    if request.user.role == 'doctor' and hasattr(request.user, 'doctor_profile'):
        context['doctor_profile'] = request.user.doctor_profile
    elif request.user.role == 'client' and hasattr(request.user, 'client_profile'):
        context['client_profile'] = request.user.client_profile

    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})