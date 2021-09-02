from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.models import ModelForm
from django.utils.regex_helper import Choice
from .models import CheckboxChoices, Product

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg. kvm@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        
class FilterForm(forms.Form):
    camera_category = forms.MultipleChoiceField(label="Категория", required=False, 
        choices=CheckboxChoices.CATEGORY_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    corpus = forms.MultipleChoiceField(label="Тип корпуса", required=False, 
        choices=CheckboxChoices.CORPUS_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    brand = forms.MultipleChoiceField(label="Бренд", required=False, 
        choices=CheckboxChoices.BRAND_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    resolution = forms.MultipleChoiceField(label="Разрешение", required=False, 
        choices=CheckboxChoices.RESOLUTION_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    zoom = forms.MultipleChoiceField(label="Оптическое увеличение", required=False, 
        choices=CheckboxChoices.ZOOM_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    sensor = forms.MultipleChoiceField(label="Оптический сенсор", required=False, 
        choices=CheckboxChoices.SENSOR_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    protection = forms.MultipleChoiceField(label="Защита от пыли/влаги", required=False, 
        choices=CheckboxChoices.PROTECTION_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    ik = forms.MultipleChoiceField(label="ИК/EXIR подсветка", required=False, 
        choices=CheckboxChoices.IK_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    has_micro = forms.MultipleChoiceField(label="Аудиовыход", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    has_wifi = forms.MultipleChoiceField(label="Wi-Fi", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    has_microsd = forms.MultipleChoiceField(label="MicroSD", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    focal_length = forms.MultipleChoiceField(label="Фокусное расстояние объектива", required=False, 
        choices=CheckboxChoices.FOCAL_LENGTH, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    lens_type = forms.MultipleChoiceField(label="Тип объектива", required=False, 
        choices=CheckboxChoices.LENS_TYPE_CHOCIES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}))
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)