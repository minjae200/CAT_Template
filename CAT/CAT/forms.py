from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label='user name', max_length=100, required=False,
                widget=forms.TextInput(attrs={'placeholder': 'AD ID', 'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=100, required=False,
                widget=forms.TextInput(attrs={'placeholder': 'AD Password', 'class': 'form-control'}))