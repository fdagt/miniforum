from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import views as auth_views
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login
from .forms import ThreadForm, PostForm
from .models import Thread, Post

class IndexView(generic.base.RedirectView):
    permanent = True
    query_string = False
    pattern_name = 'miniforum:thread_index'

class ThreadIndexView(generic.ListView):
    model = Thread
    paginate_by = 20
    template_name = 'miniforum/thread_index.html'
    ordering = '-updated_at'

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
            post = Post(thread=thread, content=form.cleaned_data['content'])
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
        thread = get_object_or_404(Thread, pk=self.kwargs['pk'])
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
            post = Post(thread=thread, content=form.cleaned_data['content'])
            if self.request.user.is_authenticated:
                post.user = self.request.user
            thread.save() # updated_atを更新
            post.save()
        return HttpResponseRedirect(reverse('miniforum:thread_detail', args=(thread.pk,)))

class LoginView(auth_views.LoginView):
    template_name = 'miniforum/login.html'
    next_page = reverse_lazy('miniforum:thread_index')
    
class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('miniforum:thread_index')

class RegisterView(generic.FormView):
    template_name = 'miniforum/register.html'
    form_class = auth_forms.UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('miniforum:thread_index'))
