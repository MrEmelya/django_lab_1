import os
import json
import datetime
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import NewsForm

# Путь к файлу с данными
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'news.json')

def ensure_data_file():
    """Проверяет, существует ли папка и файл данных. Если нет - создает."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_news():
    """Читает JSON и возвращает список словарей."""
    ensure_data_file()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_news(news_list):
    """Перезаписывает JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

def home_view(request):
    """Главная страница со списком новостей."""
    news_list = load_news()
    
    # Сортируем в обратном хронологическом порядке (от новых к старым)
    # Используем ключ 'date', а если даты совпадают - по 'id'
    news_list.sort(key=lambda x: (x['date'], x['id']), reverse=True)
    
    # Получаем сегодняшнюю дату в формате YYYY-MM-DD
    today = datetime.date.today().isoformat()
    
    context = {
        'news_list': news_list,
        'today': today
    }
    return render(request, 'home.html', context)

def news_detail_view(request, news_id):
    """Страница отдельной новости."""
    news_list = load_news()
    
    # Ищем новость по id
    news_item = next((n for n in news_list if n['id'] == news_id), None)
    
    if news_item is None:
        raise Http404("Новость не найдена")
        
    return render(request, 'news_detail.html', {'news': news_item})

def add_news_view(request):
    """Добавление новости."""
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news_list = load_news()
            
            # Генерируем новый ID
            max_id = max((n['id'] for n in news_list), default=0) + 1
            
            # Создаем словарь с новостью
            new_news = {
                'id': max_id,
                'title': form.cleaned_data['title'],
                'summary': form.cleaned_data['summary'],
                'content': form.cleaned_data['content'],
                'date': datetime.date.today().isoformat() # Автогенерация даты
            }
            
            news_list.append(new_news)
            save_news(news_list)
            
            return redirect('success')
    else:
        form = NewsForm()
        
    return render(request, 'add_news.html', {'form': form})

def success_view(request):
    """Страница успешного добавления."""
    return render(request, 'success.html')
