from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, views as auth_views
from .forms import ThreadForm, PostForm, ReportForm, LoginForm, RegisterForm
from .models import Thread, Post, Report

def get_ip_address(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']
    
class IndexView(generic.base.RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'miniforum:thread_index'

class ThreadIndexView(generic.ListView):
    model = Thread
    paginate_by = 20
    template_name = 'miniforum/thread_index.html'
    ordering = '-updated_at'

    def get_queryset(self):
        return Thread.objects.filter(deleted_at=None).order_by('-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        context['paginator_range'] = paginator.get_elided_page_range(page_obj.number, on_ends=1)
        return context
        
class ThreadCreateView(generic.FormView):
    template_name = 'miniforum/thread_create.html'
    form_class = ThreadForm
    
    def form_valid(self, form):
        with transaction.atomic():
            thread = Thread(title=form.cleaned_data['title'])
            thread.save()
            post = Post(thread=thread, content=form.cleaned_data['content'], ip_address=get_ip_address(self.request))
            if self.request.user.is_authenticated:
                post.user = self.request.user
            post.save()
        return HttpResponseRedirect(reverse('miniforum:thread_detail', args=(thread.pk,)))

class ThreadDetailView(generic.base.RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'miniforum:post_index'

class PostIndexView(generic.ListView):
    paginate_by = 100
    template_name = 'miniforum/post_index.html'

    def get_queryset(self):
        thread = get_object_or_404(Thread, pk=self.kwargs['pk'], deleted_at=None)
        return thread.post_set.order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = get_object_or_404(Thread, pk=self.kwargs['pk'])
        paginator = context['paginator']
        page_obj = context['page_obj']
        context['paginator_range'] = paginator.get_elided_page_range(page_obj.number, on_ends=1)
        return context
    
class PostCreateView(generic.FormView):
    template_name = 'miniforum/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = get_object_or_404(Thread, pk=self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        with transaction.atomic():
            thread = get_object_or_404(Thread, pk=self.kwargs['pk'])
            post = Post(thread=thread, content=form.cleaned_data['content'], ip_address=get_ip_address(self.request))
            if self.request.user.is_authenticated:
                post.user = self.request.user
            thread.save() # updated_atを更新
            post.save()
        return HttpResponseRedirect(reverse('miniforum:thread_detail', args=(thread.pk,)))

class ReportCreateView(generic.FormView):
    template_name = 'miniforum/report_create.html'
    form_class = ReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = get_object_or_404(Thread, pk=self.kwargs['pk'], deleted_at=None)
        return context
        
    def form_valid(self, form):
        with transaction.atomic():
            thread = get_object_or_404(Thread, pk=self.kwargs['pk'], deleted_at=None)
            report = Report(thread=thread, content=form.cleaned_data['content'], ip_address=get_ip_address(self.request))
            if self.request.user.is_authenticated:
                report.user = self.request.user
            report.save()
        return HttpResponseRedirect(reverse('miniforum:report_done', args=(thread.pk,)))
    
class ReportDoneView(generic.TemplateView):
    template_name = 'miniforum/report_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = get_object_or_404(Thread, pk=self.kwargs['pk'], deleted_at=None)
        return context

class LoginView(generic.FormView):
    template_name = 'miniforum/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('miniforum:thread_index'))
        else:
            form.add_error(None, "ユーザー名かパスワードが間違っています。")
            return super().form_invalid(form)

class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('miniforum:thread_index')

class RegisterView(generic.FormView):
    template_name = 'miniforum/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        with transaction.atomic():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error(None, "既に存在しているユーザー名です。")
                return super().form_invalid(form)
            user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password'])
        login(self.request, user)
        return HttpResponseRedirect(reverse('miniforum:thread_index'))
