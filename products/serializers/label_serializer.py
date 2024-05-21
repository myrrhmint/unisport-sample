from rest_framework import serializers

from products.models import Label

__all__ = ["LabelSerializer", "ProductLabelSerializer"]


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        read_only_fields = ["id"]
        fields = [
            "name",
            "priority",
            "color",
            "background_color",
            "active",
        ] + read_only_fields


class ProductLabelSerializer(serializers.ModelSerializer):
    label_id = serializers.IntegerField(source="id")

    class Meta:
        model = Label
        read_only_fields = ["name", "priority", "color", "background_color", "active"]
        fields = ["label_id"] + read_only_fields
