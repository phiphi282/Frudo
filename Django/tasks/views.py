from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from django.conf import settings
import logging
import re

from .models import Task, Comment, Label
from .forms import CreateTaskForm, CreateCommentForm, CreateLabelForm, ProtocolParseForm
# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    """This view shows the list of tasks.

    Attributes:
        template_name: The URL of the respective HTML template file
        context_object_name: The name of the list in the template
    """
    template_name = 'tasks/listopentasks.html'
    context_object_name = 'tasks_list'

    def get_queryset(self):
        """This function retrieves all tasks according to a filter.
        """
        filter = self.request.GET.get('filter', '')
        return Task.objects.filter(is_finished=False, task_text__contains=filter).order_by('finished_date')

class ClosedTasksView(LoginRequiredMixin, generic.ListView):
    """ This view shows the list of closed tasks

    Attributes
        template_name: The path to the respective HTML template file
        context_object_name: The name of the list in the template
    """
    template_name = 'tasks/listclosedtasks.html'
    context_object_name = 'tasks_list'

    def get_queryset(self):
        """This function retrieves all tasks according to a filter.
        """
        filter = self.request.GET.get('filter', '')
        return Task.objects.filter(is_finished=True, task_text__contains=filter).order_by('finished_date')

class DetailView(LoginRequiredMixin, generic.CreateView):
    """This view shows the details of a certain task.

    Attributes:
        model: The model to be used (in this case, a Task)
        template_name: The URL of the respective HTML template file
        form_class: The form class used in this view
    """
    model = Task
    template_name = 'tasks/detail.html'
    form_class = CreateCommentForm

    def get_success_url(self):
        """This function retrieves the URL to which the user is redirected on successful use of the view.
        """
        return reverse('tasks:detail', args=(self.get_object().pk,))

    def get_context_data(self, **kwargs):
        """This function retrieves the contextual data for a given task (i. e., task, members (assignees), comments, labels).
        """
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object()
        context['members'] = User.objects.filter(task=self.get_object())
        context['comments'] = Comment.objects.filter(comment_task=self.get_object())
        context['labels'] = Label.objects.filter(task=self.get_object())
        return context

    def form_valid(self, form):
        """This function checks whether the form is filled in correctly or not.
        """
        self.obj = form.save(commit=False)
        self.obj.comment_task = self.get_object()
        self.obj.comment_date = timezone.now()
        self.obj.comment_user = self.request.user
        self.obj.save()
        response = super(DetailView, self).form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))

class NewTaskView(LoginRequiredMixin, generic.CreateView):
    """This view shows the form for creating a new task.

    Attributes:
        model: The model to be used (in this case, a Task)
        template_name: The URL of the respective HTML template file
        form_class: The form class used in this view
        success_url: The URL to which the user is redirected on successful use of the view
    """
    model = Task
    template_name = 'tasks/newtask.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks:index')

    def get_context_data(self, **kwargs):
        """This function retrieves the contextual data needed for creating a new task (i. e., members (possible assignees), labels).
        """
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all
        context['members'] = User.objects.all

        return context;

    def form_valid(self, form):
        """This function checks whether the form is filled in correctly or not.
        """
        self.obj = form.save(commit=False)
        self.obj.creation_date = timezone.now()
        self.obj.save()
        #response = super(NewTaskView, self).form_valid(form)

        #mail = EmailMessage('Test', self.obj.assignedTo, 'phillip@dangernoodle', ['phillip@freitagsrunde.org'])
        #mail.send()
        return super(NewTaskView, self).form_valid(form)
        #return response

class NewLabelView(LoginRequiredMixin, generic.CreateView):
    """This view shows the form for creating a new label.

    Attributes:
        model: The model to be used (in this case, a Label)
        template_name: The URL of the respective HTML template file
        form_class: The form class used in this view
        success_url: The URL to which the user is redirected on successful use of the view
    """
    model = Label
    template_name = 'tasks/newlabel.html'
    form_class = CreateLabelForm
    success_url = reverse_lazy('tasks:index')

class EditTaskView(LoginRequiredMixin, generic.UpdateView):
    """This view shows the form for creating a new label.

    Attributes:
        model: The model to be used (in this case, a Label)
        template_name: The URL of the respective HTML template file
        form_class: The form class used in this view
        success_url: The URL to which the user is redirected on successful use of the view
    """
    model = Task
    template_name = 'tasks/edittask.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        """This function checks whether the form is filled in correctly or not.
        """
        #save cleaned post data
        self.object = form.save()
        return super(EditTaskView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """This function retrieves the contextual data needed for creating a new task (i. e., labels, members (possible assignees), due date and current labels and members (assignees)).
        """
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all
        context['members'] = User.objects.all
        context['finished_date'] = self.get_object().finished_date
        context['curr_labels'] = self.get_object().labels.all
        context['curr_members'] = self.get_object().assignedTo.all

        return context;

class ImpressumView(generic.TemplateView):
    """This view shows the imprint.
    """
    template_name = 'tasks/impressum.html'


def finishTask(request, task_id):
    """This function closes a task upon user request.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tasks:index'))
    task = get_object_or_404(Task, pk=task_id)

    task.is_finished = True;
    task.save()

    return HttpResponseRedirect(reverse('tasks:index'))

def reopen(request, task_id):
    """This function reopens a task upon user request.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tasks:closedTasks'))
    task = get_object_or_404(Task, pk=task_id)

    task.is_finished = False;
    task.save()

    return HttpResponseRedirect(reverse('tasks:closedTasks'))

class ProtocolParse(LoginRequiredMixin, generic.FormView):
    """This view shows the form for having a protocol parsed and adding its contents to the todo database.

    Attributes:
        template_name: The URL of the respective HTML template file
        form_class: The form class used in this view
        success_url: The URL to which the user is redirected on successful use of the view
    """
    template_name = 'tasks/newprotocol.html'
    form_class = ProtocolParseForm
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        """This function checks whether the form is filled in correctly or not.
        """
        text = self.request.POST['protocol_text']
        rows = re.split('\n', text)
        email_task_content = ""
        description = ""
        text = ""
        email_content = ""
        for row in rows:
            #depricated for etherpad: if row.startswith('* '):
            if row.startswith('####: '):
                if text != "":
                    add_topic = "Thema in der Sitzung: " + description + "\n" + email_task_content
                    email_task_content = ""
                    email_content += add_topic
                    text = ""

                description = row[5:]

            if 'TODO' in row:
                todo = row[row.find('TODO'):]
                if ':' in todo:
                    users, text = todo.split(':', 1)
                    if len(users) < 6:
                        users = "TODO alle:"

                    task = Task.objects.create(task_text=text,
                                               task_description='zum Thema in der Sitzung: '+description,
                                               finished_date=(timezone.now() + timedelta(days=7)),
                                               creation_date=timezone.now(),
                                               is_finished=False,
                                               important=False)

                    email_task_content += "  TODO:          " + text + "\n  Beauftragte(r): " + users[5:] + "\n\n"



                    for user in users.split():
                        try:
                            user_obj = User.objects.get(username=user.lower())
                            task.assignedTo.add(user_obj)
                        except User.DoesNotExist:
                            None

        email_content = "Heyho,\n\nin der Sitzung wurden neue Aufgaben verteilt.\n\n" + email_content + "Euch noch ein frohes Schaffen\nFrudo"
        mail = EmailMessage('SitzungsTODOs', email_content, settings.EMAIL_HOST_USER, [settings.EMAIL_GROUP_RECEIVE])
        if (settings.EMAIL_HOST != "example.com"):
            mail.send()
        return super(ProtocolParse, self).form_valid(form)
