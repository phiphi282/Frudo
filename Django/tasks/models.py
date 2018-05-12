from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Label(models.Model):
    """This class provides a label for differentiating tasks into groups.

    Attributes:
        label_text: The name of the label
        label_description: The description of the label
        label_color: The color of the label
    """

    label_text = models.CharField(max_length=32)
    label_description = models.CharField(max_length=129, blank=True, default='')
    label_color = models.CharField(max_length=10)

    def __str__(self):
        return self.label_text

class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['label_text', 'label_description', 'label_color']

    label_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    label_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    label_color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class ProtocolParseForm(forms.Form):
    protocol_url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    protocol_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=False)

    def clean(self):
        check_form = super(ProtocolParseForm, self).clean()

        if not any(
            check_form.get(x, '')
            for x in (
                'protocol_url',
                'protocol_text',
            )
        ):
            self._errors['protocol_url'] = self.error_class([("You must enter at least the protocol url or text")])
            self._errors['protocol_text'] = self.error_class([("You must enter at least the protocol url or text")])


# Create your models here.
class Task(models.Model):
    """This class represents tasks.

    Attributes:
        task_text: The task title
        task_description: A more detailed description of the task
        finished_date: The due date of the task
        creation_date: The date on which the task was created
        important: A boolean value whether the task is important or normal
        assignedTo: The list of accounts to which the task is assigned
        labels: The list of labels for this task
        progress: An integer value (0..100) to describe the progress of the task in percentage
    """

    task_text = models.CharField(max_length=64)
    task_description = models.CharField(max_length=512)
    finished_date = models.DateField()
    creation_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    important = models.BooleanField()
    assignedTo = models.ManyToManyField(User, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.task_text

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'task_description', 'finished_date', 'assignedTo', 'labels', 'important', 'progress']

    task_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    task_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    #assignedTo = forms.MultiWidget(widget=forms.CheckboxSelectMultiple(attrs={'class':'js-example-basic-multiple'}))

    def clean_finished_date(self):
        finished = self.cleaned_data['finished_date']

        if finished < timezone.now().date():
            raise ValidationError("Date too early")

        return finished

class Subtask(models.Model):
    """Currently not used."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask_text = models.CharField(max_length=512)
    finished_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

class Comment(models.Model):
    """This class represents comments given on tasks.

    Attributes:
        comment_text: The text of the comment
        comment_user: The user who commented
        comment_task: The task to which the comment refers
        comment_date: The date on which the comment was given
    """
    comment_text = models.CharField(max_length=512)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_date = models.DateTimeField()

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
