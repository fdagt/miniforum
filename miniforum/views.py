from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db import transaction

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

class ThreadDetailView(generic.DetailView):
    model = Thread
    template_name = 'miniforum/thread_detail.html'

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
