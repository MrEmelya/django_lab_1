from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    summary = models.CharField(max_length=300, verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Текст новости")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-date_created'] # Сортировка от новых к старым по умолчанию
