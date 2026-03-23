"""
Definition of forms.
"""

from django import forms
from .models import RATING_CHOICES 
from .models import LIKED_CHOICES 
from .models import AGE_CHOICES 

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class ReviewForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Email')

    liked = forms.MultipleChoiceField(
        label='Что вам особенно понравилось?',
        widget=forms.CheckboxSelectMultiple,
        choices= LIKED_CHOICES,
    )
    rating = forms.ChoiceField(
        choices= RATING_CHOICES, 
        label='Оцените нашу работу', 
        widget=forms.RadioSelect
    )
    # Один вариант из списка (выпадающее меню)
    age = forms.ChoiceField(
        label='Возраст ребёнка',
        choices=AGE_CHOICES
    )


    message = forms.CharField(widget=forms.Textarea, label = 'Комментарий')
    consent = forms.BooleanField(label='Согласие на обработку', required=True)




