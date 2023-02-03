from django.db import models


class Device(models.Model):
    on_time = models.IntegerField(default=0)
    off_time = models.IntegerField(default=0)

