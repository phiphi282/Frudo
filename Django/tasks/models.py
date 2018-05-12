from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
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
