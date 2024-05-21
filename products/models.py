from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=255)
    priority = models.IntegerField()
    color = models.CharField(max_length=7)
    background_color = models.CharField(max_length=7)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id} {self.name}"


class Product(models.Model):
    product_id = models.IntegerField()
    style = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    relative_url = models.CharField(max_length=255)
    image = models.URLField(max_length=500)
    delivery = models.CharField(max_length=50)
    online = models.BooleanField()
    active = models.BooleanField()
    labels = models.ManyToManyField(Label, related_name="products")
    is_customizable = models.BooleanField()
    paid_print = models.BooleanField()
    is_exclusive = models.BooleanField()
    customization_template_id = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10)
    url = models.URLField(max_length=500)
    attributes = models.JSONField()

    def __str__(self):
        return f"{self.id} {self.name}"


class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="stock", on_delete=models.CASCADE)
    sku_id = models.IntegerField()
    size_id = models.IntegerField()
    barcode = models.CharField(max_length=20)
    order_by = models.IntegerField()
    name = models.CharField(max_length=50)
    name_short = models.CharField(max_length=50)
    stock_info = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recommended_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    supplier = models.CharField(max_length=50)
    is_marketplace = models.BooleanField()
    availability = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} {self.name}"
