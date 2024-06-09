

from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
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