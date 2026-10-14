from django import forms
from django.core.exceptions import ValidationError
from apps.analytics.models import Review
from apps.clients.models import Appointment
from datetime import date, datetime

from apps.core.models import News


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} звезд{'а' if i == 1 else 'ы' if i <= 4 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Оценка'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Напишите ваш отзыв...'}),
        label='Текст отзыва',
        min_length=10,
        max_length=1000
    )

    class Meta:
        model = Review
        fields = ['rating', 'text']

    def clean_text(self):
        text = self.cleaned_data['text']
        forbidden_words = ['спам', 'реклама']
        for word in forbidden_words:
            if word in text.lower():
                raise ValidationError(f'Текст отзыва содержит запрещенное слово: {word}')
        return text


class NewsForm(forms.ModelForm):
    """Форма для создания и редактирования новостей"""

    class Meta:
        model = News
        fields = ['title', 'short_description', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок новости'}),
            'short_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Краткое описание (одно предложение)'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Полное содержание новости'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_published':
                self.fields[field].widget.attrs.update({'class': 'form-control'})