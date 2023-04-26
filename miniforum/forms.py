from django import forms
from django.contrib.auth.models import User

class ThreadForm(forms.Form):
    template_name = 'miniforum/form.html'
    title = forms.CharField(max_length=100, label="スレッド名", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(max_length=1000, label="投稿内容", widget=forms.Textarea(attrs={'rows':6, 'class': 'form-control'}))
    
class PostForm(forms.Form):
    template_name = 'miniforum/form.html'
    content = forms.CharField(max_length=1000, label="投稿内容", widget=forms.Textarea(attrs={'rows':6, 'class': 'form-control'}))

class ReportForm(forms.Form):
    template_name = 'miniforum/form.html'
    content = forms.CharField(max_length=1000, label="通報内容", widget=forms.Textarea(attrs={'rows':6, 'class': 'form-control'}))

class LoginForm(forms.Form):
    template_name = 'miniforum/form.html'
    username = forms.CharField(required=True, max_length=150, label="ユーザー名", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, label="パスワード", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    template_name = 'miniforum/form.html'
    username = forms.CharField(required=True, max_length=150, label="ユーザー名", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, label="パスワード", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(required=True, label="パスワード（再入力）", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def is_valid(self):
        valid = super().is_valid()
        if self.data['password'] != self.data['password_confirm']:
            self.add_error('password_confirm', "再入力パスワードが一致しませんでした。")
            return False
        else:
            return valid
