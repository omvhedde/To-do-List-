from distutils.log import Log
from typing import List
from django.shortcuts import render
from django.views.generic.list import  ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView 

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name="task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(completed=False)
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task 
    context_object_name='task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description','completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description','completed']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')