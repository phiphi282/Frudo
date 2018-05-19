from django.test import TestCase

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Task, Label

# Create your tests here.

def create_task(task_text, task_description, finished_date, creation_date, is_finished, important, progress):
    return Task.objects.create(task_text=task_text, task_description=task_description, finished_date=finished_date, creation_date=creation_date, is_finished=is_finished, important=important)

def create_label(label_text, label_description, label_color):
    return Label.objects.create(label_text=label_text, label_description=label_description, label_color=label_color)

class CreateTaskTests(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='user1', password='12345')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertRedirects(response, '/account/login/?next=/tasks/')

    def test_basictask(self):
        login = self.client.login(username='user1', password='12345')
        time = timezone.now()
        create_task("test", "testi", time, time, False, False)
        response = self.client.get(reverse('tasks:index'))
        self.assertQuerysetEqual(
            response.context['tasks_list'],
            ['<Task: test>']
        )
