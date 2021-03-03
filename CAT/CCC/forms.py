from django import forms
from CCC.Helper.DateHelper import *
# from datetime import datetime, date, timedelta
import datetime


class ModuleForm(forms.Form):
    name = forms.CharField(label='module name', max_length=100, required=False,
                widget=forms.TextInput(attrs={'placeholder': 'module name', 'class': 'form-control'}))
    tag = forms.CharField(label='tag', max_length=100, required=False,
                widget=forms.TextInput(attrs={'placeholder': 'tag', 'class': 'form-control'}))
    hash_value = forms.CharField(label='hash', max_length=100, required=False,
                widget=forms.TextInput(attrs={'placeholder': 'hash', 'class': 'form-control'}))

class JobForm(forms.Form):
    BRANCH_CHOICES = (
        ("45.kalaupapa", "45.kalaupapa"),
        ("webos4tv", "webos4tv"),
        ("jardine", "jardine"),
        ("jcl4tv", "jcl4tv"),
    )
    branch = forms.ChoiceField(label='Branch', choices=BRANCH_CHOICES, required=False)
