from django.db import models

# Create your models here.


class Image(models.Model):
    def __init__(self, image):
        self.image = image
        self.isUsed = False
    image = models.CharField(max_length=100000)
    isUsed = models.BooleanField

    def __str__(self):
        return self.image
