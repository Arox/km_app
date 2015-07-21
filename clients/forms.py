# -*- coding: utf-8 -*-
from django import forms

class ClientFindForm(forms.Form):
    find_text = forms.CharField(max_length=101, label='', required=False)
