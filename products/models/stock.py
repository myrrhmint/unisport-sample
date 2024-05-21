from django.db import models


__all__ = ["Stock"]


class Stock(models.Model):
    product = models.ForeignKey(
        "Product", related_name="stock", on_delete=models.CASCADE
    )
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
