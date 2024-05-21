from django.db import models


__all__ = ["Product"]


class Product(models.Model):
    product_id = models.IntegerField()
    style = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    relative_url = models.CharField(max_length=255)
    image = models.URLField(max_length=500)
    delivery = models.CharField(max_length=50)
    online = models.BooleanField()
    active = models.BooleanField()
    labels = models.ManyToManyField("Label", related_name="products")
    is_customizable = models.BooleanField()
    paid_print = models.BooleanField()
    is_exclusive = models.BooleanField()
    customization_template_id = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10)
    url = models.URLField(max_length=500)
    attributes = models.JSONField()

    def __str__(self):
        return f"{self.id} {self.name}"
