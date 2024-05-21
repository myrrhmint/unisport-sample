from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import status
from products.models import Product, Stock, Label
from products.serializers import (
    ProductLabelSerializer,
    ProductSerializer,
    StockSerializer,
    LabelSerializer,
)
from django.db.models import Min


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(min_stock_price=Min("stock__price")).order_by(
            "min_stock_price"
        )


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


# Used to retrieve and manipulate all labels
class LabelViewset(viewsets.ModelViewSet):
    serializer_class = LabelSerializer

    def get_queryset(self):
        return Label.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = LabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        label = Label.objects.create(**serializer.data)
        return Response(LabelSerializer(label).data, status=status.HTTP_201_CREATED)


# Used to retrieve the labels tied to a specific product
class ProductLabelViewset(
    viewsets.mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProductLabelSerializer

    def get_queryset(self):
        try:
            product = Product.objects.get(pk=int(self.kwargs["product_pk"]))
            return Label.objects.filter(products__id=product.id)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Adds the label specified in the request to the product specified in the URL
        """
        serializer = ProductLabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            label = Label.objects.get(pk=serializer.data["label_id"])
        except Label.DoesNotExist:
            raise NotFound(detail="Label not found")
        try:
            product = Product.objects.get(pk=int(self.kwargs["product_pk"]))
            product.labels.add(label)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
        return Response(
            ProductLabelSerializer(label).data, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        """
        Removes the label specified in the URL from the product specified in the URL
        """
        try:
            product = Product.objects.get(pk=int(self.kwargs["product_pk"]))
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
        try:
            label = Label.objects.get(pk=int(self.kwargs["pk"]))
        except Label.DoesNotExist:
            raise NotFound(detail="Label not found")
        product.labels.remove(label)
        return Response(status=status.HTTP_204_NO_CONTENT)
