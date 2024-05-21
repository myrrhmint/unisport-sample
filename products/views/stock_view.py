from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import status
from products.models import Product, Stock, Label
from products.serializers import (
    StockSerializer,
)
from django.db.models import Min

__all__ = ["StockViewset"]


# Used to retrieve and manipulate the stock of a specific product
class StockViewset(viewsets.ModelViewSet):
    serializer_class = StockSerializer

    def get_queryset(self):
        try:
            product = Product.objects.get(pk=int(self.kwargs["product_pk"]))
            return Stock.objects.filter(product=product).order_by("size_id")
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")

    def create(self, request, *args, **kwargs):
        """
        Creates a new stock item for the product specified in the URL
        """
        serializer = StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = Product.objects.get(pk=int(self.kwargs["product_pk"]))
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
        stock = Stock.objects.create(**serializer.data, product=product)
        return Response(StockSerializer(stock).data, status=status.HTTP_201_CREATED)
