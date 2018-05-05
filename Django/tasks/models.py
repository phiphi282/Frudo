from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Label(models.Model):
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

# Create your models here.
class Task(models.Model):
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
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask_text = models.CharField(max_length=512)
    finished_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

class Comment(models.Model):
    comment_text = models.CharField(max_length=512)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_date = models.DateTimeField()

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
