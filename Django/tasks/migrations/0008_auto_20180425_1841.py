# Generated by Django 2.0.4 on 2018-04-25 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20180425_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='finished_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
