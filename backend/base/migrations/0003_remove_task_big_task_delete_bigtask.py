# Generated by Django 5.0.1 on 2024-05-30 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_bigtask_task_big_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='big_task',
        ),
        migrations.DeleteModel(
            name='BigTask',
        ),
    ]