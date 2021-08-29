from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import CheckboxChoices

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg. kvm@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')

class FilterForm(forms.Form):
    corpus_field = forms.MultipleChoiceField(label="Тип корпуса", required=False, 
        choices=CheckboxChoices.CORPUS_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))

    brand_field = forms.MultipleChoiceField(label="Бренд", required=False, 
        choices=CheckboxChoices.BRAND_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))

    resolution_field = forms.MultipleChoiceField(label="Разрешение", required=False, 
        choices=CheckboxChoices.RESOLUTION_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))

    zoom_field = forms.MultipleChoiceField(label="Оптическое увеличение", required=False, 
        choices=CheckboxChoices.ZOOM_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    sensor_field = forms.MultipleChoiceField(label="Оптический сенсор", required=False, 
        choices=CheckboxChoices.SENSOR_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    protection_field = forms.MultipleChoiceField(label="Аудиовход", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    ik_field = forms.MultipleChoiceField(label="Аудиовыход", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    sensitivity_field = forms.MultipleChoiceField(label="MicroSD", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    vand_protection_field = forms.MultipleChoiceField(label="Защита от пыли/влаги", required=False, 
        choices=CheckboxChoices.PROTECTION_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    has_audio_input_field = forms.MultipleChoiceField(label="ИК/EXIR подсветка", required=False, 
        choices=CheckboxChoices.IK_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    has_audio_output_field = forms.MultipleChoiceField(label="Наличие тревожных входов", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    has_wifi_field = forms.MultipleChoiceField(label="Наличие тревожных выходов", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    has_microsd_field = forms.MultipleChoiceField(label="Чувствительность", required=False, 
        choices=CheckboxChoices.SENSITIVITY_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    has_alarm_input_field  = forms.MultipleChoiceField(label="Защита от вандализма", required=False, 
        choices=CheckboxChoices.VAND_PROT_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))
    
    has_alarm_output_field  = forms.MultipleChoiceField(label="Wi-Fi", required=False, 
        choices=CheckboxChoices.YES_OR_NO_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}))

