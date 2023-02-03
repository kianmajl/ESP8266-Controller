from django.db import models


class Color(models.Model):
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()

