from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import ThreadForm
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
        thread = Thread(title=form.cleaned_data['title'])
        thread.save()
        return HttpRedirectResponse(reverse('miniforum:thread_detail', args=(thread.pk,)))

def thread_detail(request, pk):
    thread = Thread.objects.get(pk=pk)
    return HttpResponse(thread.title, content_type='text/plain; charset="utf-8"')
