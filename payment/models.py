from django.db import models

# Create your models here.


class Payment(models.Model):
    method = models.CharField(max_length=50, blank=False)
