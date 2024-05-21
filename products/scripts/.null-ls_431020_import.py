import requests
import json
from django.conf import settings
from products.models import Product, Label, Stock
from products.helpers.base_models import ProductItem, LabelItem, StockItem, Price


def cleanup() -> None:
    Product.objects.all().delete()
    Label.objects.all().delete()


def create_product(product: ProductItem) -> Product:
    product_model = Product.objects.create(
        product_id=product.product_id,
        style=product.style,
        name=product.name,
        relative_url=product.relative_url,
        image=product.image,
        delivery=product.delivery,
        online=product.online,
        active=product.active,
        is_customizable=product.is_customizable,
        paid_print=product.paid_print,
        is_exclusive=product.is_exclusive,
        customization_template_id=product.customization_template_id,
        currency=product.currency,
        url=product.url,
        attributes=product.attributes,
    )
    for label in product.labels:
        label_model = Label.objects.create(
            name=label.name,
            priority=label.priority,
            color=label.color,
            background_color=label.background_color,
            active=label.active,
        )
        product_model.labels.add(label_model)
    for stock in product.stock:
        Stock.objects.create(
            product=product_model,
            sku_id=stock.sku_id,
            size_id=stock.size_id,
            barcode=stock.barcode,
            order_by=stock.order_by,
            name=stock.name,
            name_short=stock.name_short,
            stock_info=stock.stock_info,
            price=stock.price,
            recommended_retail_price=stock.recommended_retail_price,
            discount_percentage=stock.discount_percentage,
            supplier=stock.supplier,
            is_marketplace=stock.is_marketplace,
            availability=stock.availability,
        )
    return product_model


def print_product_info(product: Product) -> None:
    print(f"Created product: {product.id} - {product.name}")
    print(f"- Labels: {[l for l in product.labels.all()]}")
    print(f"- Stock: {[s for s in product.stock.all()]}")


def run():
    # Load import URL from environment variable UNISPORT_IMPORT_URL
    import_url = settings.UNISPORT_IMPORT_URL
    response = requests.get(import_url)
    data = response.json()

    products = data["products"]
    for product in products:
        validated_product = ProductItem(**product)
        product_model = create_product(validated_product)
        print_product_info(product_model)
