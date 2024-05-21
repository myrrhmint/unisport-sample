from rest_framework import serializers

from products.models import Stock

__all__ = ["StockSerializer"]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        read_only_fields = ["id", "product"]
        fields = [
            "sku_id",
            "size_id",
            "barcode",
            "order_by",
            "name",
            "name_short",
            "stock_info",
            "price",
            "recommended_retail_price",
            "discount_percentage",
            "supplier",
            "is_marketplace",
            "availability",
        ] + read_only_fields
