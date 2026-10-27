from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import News
from .forms import NewsForm, UserRegisterForm, UserUpdateForm

def home_view(request):
    """Главная страница со списком новостей и пагинацией."""
    news_list = News.objects.all()
    
    # Настраиваем пагинацию: по 3 новости на страницу
    paginator = Paginator(news_list, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {'page_obj': page_obj})

def news_detail_view(request, news_id):
    """Детальная страница новости."""
    news = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news})

@login_required
def news_create_view(request):
    """Добавление новости (только для авторизованных)."""
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user # Привязываем автора
            news.save()
            messages.success(request, 'Новость успешно добавлена!')
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'form': form, 'title': 'Добавить новость'})

@login_required
def news_edit_view(request, news_id):
    """Редактирование новости (только для автора)."""
    news = get_object_or_404(News, id=news_id)
    
    # Проверка прав
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту новость")
        
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена!')
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_form.html', {'form': form, 'title': 'Редактировать новость'})

@login_required
def news_delete_view(request, news_id):
    """Удаление новости (только для автора)."""
    news = get_object_or_404(News, id=news_id)
    
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту новость")
        
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость удалена.')
        return redirect('home')
        
    return render(request, 'news_confirm_delete.html', {'news': news})

def register_view(request):
    """Регистрация нового пользователя."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    """Страница профиля и его редактирование."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def delete_profile_view(request):
    """Удаление аккаунта."""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Аккаунт удален.')
        return redirect('home')
    return render(request, 'profile_confirm_delete.html')
