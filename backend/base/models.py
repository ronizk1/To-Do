# from django.db import models

# # Create your models here.

# # tasks/models.py

# class BigTask(models.Model):
#     title = models.CharField(max_length=255)

# class Task(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     completed = models.BooleanField(default=False)
#     due_date = models.DateField(null=True, blank=True)
#     image = models.ImageField(upload_to='task_images/', null=True, blank=True)
#     big_task = models.ForeignKey(BigTask, related_name='subtasks', on_delete=models.CASCADE, null=True, blank=True)
    

#     def _str_(self):
#         return self.title

#     @property
#     def image_url(self):
#         if self.image:
#             return self.image.url
#         return ''

from django.db import models

# Create your models here.

# tasks/models.py

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)
    

    def _str_(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''