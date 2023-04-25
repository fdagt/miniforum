from django import forms

class ThreadForm(forms.Form):
    title = forms.CharField(max_length=100, label="スレッド名")
    content = forms.CharField(max_length=1000, label="書き込み内容", widget=forms.Textarea(attrs={'rows':6}))
    
class PostForm(forms.Form):
    content = forms.CharField(max_length=1000, label="書き込み内容", widget=forms.Textarea(attrs={'rows':6}))
