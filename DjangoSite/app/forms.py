from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class ReviewForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя', 
        min_length=2, 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'})
    )
    email = forms.EmailField(
        label='Email', 
        min_length=7,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    rating = forms.ChoiceField(
        label='Оцените нашу работу', 
        choices=[(5, 'Отлично'), (4, 'Хорошо'), (3, 'Удовлетворительно'), (2, 'Плохо')], 
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    liked = forms.MultipleChoiceField(
        label='Что вам особенно понравилось?', 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        choices=[
            ('diagnostic', 'Диагностика'),
            ('sound', 'Постановка звуков'),
            ('message', 'Логопедический массаж'),
            ('speech', 'Развитие речи'),
            ('school', 'Подготовка к школе'),
            ('other', 'Другое')
        ]
    )
    age = forms.ChoiceField(
        label='Возраст ребёнка', 
        choices=[
            ('3-4', '3-4 года'),
            ('4-5', '4-5 лет'),
            ('5-6', '5-6 лет'),
            ('6-7', '6-7 лет'),
            ('7+', 'Старше 7 лет'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    message = forms.CharField(
        label='Комментарий', 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваш отзыв...'})
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных', 
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class BootstrapRegistrationForm(UserCreationForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})
                field.help_text = ''


