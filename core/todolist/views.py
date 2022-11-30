from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse
from .forms import TaskUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.views import View
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Task


class TaskList(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "base.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("task_list")
    form_class = TaskUpdateForm

    template_name = "todo/update_task.html"


class TaskComplete(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        if object.complete is True:
            object.complete = False
        else:
            object.complete = True
        object.save()
        return redirect(self.success_url)


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

@cache_page(60*2)
def test(request):
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Tehran&APPID=274bc6d6b1bf85c2abf70a4b9e2634c3")
    return JsonResponse(response.json())