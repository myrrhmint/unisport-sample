import factory
from products.models import Product, Label, Stock


class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Faker("word")
    priority = factory.Faker("random_int")
    color = factory.Faker("hex_color")
    background_color = factory.Faker("hex_color")
    active = factory.Faker("boolean")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_id = factory.Sequence(lambda n: n)
    style = factory.Faker("word")
    name = factory.Faker("word")
    relative_url = factory.Faker("url")
    image = factory.Faker("url")
    delivery = factory.Faker("word")
    online = factory.Faker("boolean")
    active = factory.Faker("boolean")
    is_customizable = factory.Faker("boolean")
    paid_print = factory.Faker("boolean")
    is_exclusive = factory.Faker("boolean")
    customization_template_id = factory.Faker("random_int")
    currency = "DKK"
    url = factory.Faker("url")
    attributes = "{}"

    @factory.post_generation
    def labels(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.labels.add(*extracted)


class ProductWithSingleStockFactory(ProductFactory):
    @factory.post_generation
    def stock(self, create, extracted, **kwargs):
        if create:
            StockFactory(product=self)


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    product = factory.SubFactory(ProductFactory)
    sku_id = factory.Faker("random_int")
    size_id = factory.Faker("random_int")
    barcode = factory.Faker("ean")
    order_by = factory.Faker("random_int")
    name = factory.Faker("word")
    name_short = factory.Faker("word")
    stock_info = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    recommended_retail_price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    discount_percentage = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True
    )
    supplier = factory.Faker("word")
    is_marketplace = factory.Faker("boolean")
    availability = factory.Faker("word")


class ProductWithMultipleStock(ProductFactory):
    stock = factory.RelatedFactoryList(StockFactory, "product", size=10)
