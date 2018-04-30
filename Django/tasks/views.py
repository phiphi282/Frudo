from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.utils import timezone
from django.http import HttpResponseRedirect
import logging

from .models import Task, CreateTaskForm, Comment, CreateCommentForm, Label, CreateLabelForm
# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'tasks_list'

    def get_queryset(self):
        filter = self.request.GET.get('filter', '')
        return Task.objects.filter(is_finished=False, task_text__contains=filter).order_by('-finished_date')

class DetailView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = 'tasks/detail.html'
    form_class = CreateCommentForm

    def get_success_url(self):
        return reverse('tasks:detail', args=(self.get_object().pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object()
        context['members'] = User.objects.filter(task=self.get_object())
        context['comments'] = Comment.objects.filter(comment_task=self.get_object())
        context['labels'] = Label.objects.filter(task=self.get_object())
        return context

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.comment_task = self.get_object()
        self.obj.comment_date = timezone.now()
        self.obj.comment_user = self.request.user
        self.obj.save()
        response = super(DetailView, self).form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))

class NewTaskView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = 'tasks/newtask.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all
        context['members'] = User.objects.all

        return context;

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.creation_date = timezone.now()
        self.obj.save()
        #response = super(NewTaskView, self).form_valid(form)

        #mail = EmailMessage('Test', self.obj.assignedTo, 'phillip@dangernoodle', ['phillip@freitagsrunde.org'])
        #mail.send()
        return super(NewTaskView, self).form_valid(form)
        #return response

class NewLabelView(LoginRequiredMixin, generic.CreateView):
    model = Label
    template_name = 'tasks/newlabel.html'
    form_class = CreateLabelForm
    success_url = reverse_lazy('tasks:index')

class EditTaskView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/edittask.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
            #save cleaned post data
            self.object = form.save()
            return super(EditTaskView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all
        context['members'] = User.objects.all
        context['finished_date'] = self.get_object().finished_date
        context['curr_labels'] = self.get_object().labels.all
        context['curr_members'] = self.get_object().assignedTo.all

        return context;

class ImpressumView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'tasks/impressum.html'


def finishTask(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tasks:index'))
    task = get_object_or_404(Task, pk=task_id)

    task.is_finished = True;
    task.save()

    return HttpResponseRedirect(reverse('tasks:index'))
