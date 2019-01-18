from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.conf import settings

from tasks.models import Task
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Send mails to all users with unfinished polls"

    def handle(self, *args, **options):
        if (settings.EMAIL_HOST == "example.com"):
            return
        logger.info("Sending emails to users");
        users = User.objects.all()
        for user in users:
            tasks = Task.objects.filter(is_finished=False, assignedTo__in=[user.id]).distinct()
            if len(tasks) == 0:
                continue
            email_content = "Heyho,\n\n du hast noch folgende Todos offen:\n\n"
            for task in tasks:
                email_content += "    " + task.task_text + " ( https://frudo.freitagsrunde.org/tasks/" + str(task.id) + "/ )\n"

            mail = EmailMessage('Unbearbeitete ToDos', email_content, settings.EMAIL_HOST_USER, [user.username + "@" + settings.EMAIL_HOST])
            mail.send()

        unassigned = Task.objects.filter(is_finished=False, assignedTo=None)
        if len(unassigned) == 0:
                return
        email_content = "Heyho,\n\n folgende Todos sind noch offen und haben keinen Benutzer assigned:\n\n"

        for task in unassigned:
            print(task.task_text)
            email_content += "    " + task.task_text + " ( https://frudo.freitagsrunde.org/tasks/" + str(task.id) + "/ )\n"

        mail = EmailMessage('Unbearbeitete ToDos', email_content, settings.EMAIL_HOST_USER, [settings.EMAIL_GROUP_RECEIVE])
        mail.send()
