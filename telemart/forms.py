from django import forms

from .models import *


class CommentForm(forms.Form):
    text = forms.CharField(label='Type here',
                           widget=forms.TextInput(attrs={'placeholder': 'Ваш отзыв'}))


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'year', 'power', 'picture',
                  'description', 'company', 'trailer', 'hotline']