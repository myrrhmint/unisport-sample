from django.db import models

__all__ = ["Label"]


class Label(models.Model):
    name = models.CharField(max_length=255)
    priority = models.IntegerField()
    color = models.CharField(max_length=7)
    background_color = models.CharField(max_length=7)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id} {self.name}"
