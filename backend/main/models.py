from django.db import models

# Create your models here.
class TitleMovie(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    