from django import forms
from CCC.Helper.DateHelper import *
# from datetime import datetime, date, timedelta
import datetime


class ModuleForm(forms.Form):
    name = forms.CharField(label='module name', max_length=100, required=False)
    tag = forms.CharField(label='module tag', max_length=100, required=False)
    hash_value = forms.CharField(label='module hash', max_length=100, required=False)

class JobForm(forms.Form):
    branch = forms.CharField(label='Branch', max_length=100, required=False)
    build_start_time = forms.DateField(label='start_time', required=False)
