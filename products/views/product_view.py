from rest_framework import viewsets
from products.models import Product
from products.serializers import ProductSerializer
from django.db.models import Min

__all__ = ["ProductViewset"]


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(min_stock_price=Min("stock__price")).order_by(
            "min_stock_price"
        )
