import requests

class NewsAPIClient:
    def __init__(self, base_url, token=None):
        # Убираем слэш в конце, если он есть
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if token:
            self.session.headers.update({'Authorization': f'Token {token}'})
    
    def register(self, username, email, password):
        """Регистрация нового пользователя."""
        return self.session.post(f"{self.base_url}/api/users/", json={
            'username': username, 
            'email': email, 
            'password': password
        }).json()
    
    def login(self, username, password):
        """Получение токена и сохранение его в сессии."""
        resp = self.session.post(f"{self.base_url}/api/token/", json={
            'username': username, 
            'password': password
        })
        if resp.status_code == 200:
            self.session.headers.update({'Authorization': f"Token {resp.json()['token']}"})
            return True
        return False
    
    def create_news(self, title, content, summary=""):
        """Создание новости (требуется авторизация)."""
        return self.session.post(f"{self.base_url}/api/news/", json={
            'title': title, 
            'content': content, 
            'summary': summary
        }).json()
    
    def get_news(self, news_id=None, author_id=None):
        """Получение списка новостей или конкретной новости."""
        if news_id:
            url = f"{self.base_url}/api/news/{news_id}/"
        else:
            url = f"{self.base_url}/api/news/"
        
        # Фильтрация по автору
        params = {}
        if author_id:
            params['author'] = author_id
            
        return self.session.get(url, params=params).json()
    
    def update_news(self, news_id, **kwargs):
        """Частичное обновление новости."""
        return self.session.patch(f"{self.base_url}/api/news/{news_id}/", json=kwargs).json()
    
    def delete_news(self, news_id):
        """Удаление новости."""
        return self.session.delete(f"{self.base_url}/api/news/{news_id}/").status_code
