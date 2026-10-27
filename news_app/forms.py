from django import forms

class NewsForm(forms.Form):
    title = forms.CharField(
        max_length=100, 
        label="Заголовок",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'})
    )
    summary = forms.CharField(
        max_length=200, 
        label="Краткое описание",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кратко о новости'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Полный текст новости'}),
        label="Текст новости"
    )
