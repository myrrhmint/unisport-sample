from django.db.models import Max, Min
from rest_framework import serializers

from products.helpers.base_models import Price
from products.models import Product

__all__ = ["ProductSerializer", "PriceSerializer"]


class PriceSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=10)
    reccomended_retail_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class ProductSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Product
        read_only_fields = ["id", "stock", "prices", "labels"]
        fields = [
            "product_id",
            "style",
            "name",
            "relative_url",
            "image",
            "delivery",
            "online",
            "active",
            "labels",
            "is_customizable",
            "paid_print",
            "is_exclusive",
            "customization_template_id",
            "currency",
            "url",
            "attributes",
        ] + read_only_fields
        depth = 1

    def get_prices(self, obj: Product) -> Price:
        """
        Get the prices of the product based on the related stock
        """
        prices_info: Price = obj.stock.aggregate(
            min_price=Min("price"),
            max_price=Max("price"),
            reccomended_retail_price=Max("recommended_retail_price"),
            discount_percentage=Max("discount_percentage"),
        )
        prices_info["currency"] = obj.currency
        prices: Price = PriceSerializer(prices_info).data
        return prices
