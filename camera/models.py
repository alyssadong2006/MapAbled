# myapp/models.py
from django.db import models


class Photo(models.Model):
  image = models.ImageField(upload_to='photos/')
  uploaded_at = models.DateTimeField(auto_now_add=True)
  text = models.TextField(blank=True)
  rephrased_text = models.TextField(blank=True)
  audio = models.FileField(upload_to='audio/', blank=True)
