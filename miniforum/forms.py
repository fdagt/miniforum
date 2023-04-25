from django import forms

class ThreadForm(forms.Form):
    title = forms.CharField(max_length=100, label="スレッド名")
