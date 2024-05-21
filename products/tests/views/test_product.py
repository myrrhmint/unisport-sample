from django.test import TestCase
from rest_framework.reverse import reverse
from products.serializers import PriceSerializer
from products.tests.factories.products import (
    ProductWithMultipleStock,
    ProductWithSingleStockFactory,
)
from products.models import Product
from django.db.models import Max, Min


class ProductTestCase(TestCase):
    def test_no_result(self):
        response = self.client.get(reverse("products:products-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], [])

    def test_result_single_page(self):
        [ProductWithSingleStockFactory() for _ in range(10)]
        expected_products = (
            Product.objects.annotate(min_stock_price=Min("stock__price"))
            .order_by("min_stock_price")
            .all()
        )
        response = self.client.get(reverse("products:products-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertListEqual(
            [product["id"] for product in response.data["results"]],
            [product.id for product in expected_products],
        )

    def test_result_multiple_pages(self):
        [ProductWithSingleStockFactory() for _ in range(25)]
        expected_products_total = (
            Product.objects.annotate(min_stock_price=Min("stock__price"))
            .order_by("min_stock_price")
            .all()
        )
        for page in range(3):
            with self.subTest(page=page):
                response = self.client.get(
                    reverse("products:products-list"), {"page": page + 1}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    len(response.data["results"]),
                    len(expected_products_total[page * 10 : (page + 1) * 10]),
                )
            self.assertListEqual(
                [product["id"] for product in response.data["results"]],
                [
                    product.id
                    for product in expected_products_total[page * 10 : (page + 1) * 10]
                ],
            )

    def test_product_detail_not_found(self):
        response = self.client.get(reverse("products:products-detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_product_detail(self):
        product = ProductWithSingleStockFactory()
        response = self.client.get(
            reverse("products:products-detail", args=[product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], product.id)

    def test_product_create(self):
        response = self.client.post(
            reverse("products:products-list"),
            {
                "product_id": 1,
                "style": "style",
                "name": "name",
                "relative_url": "/relative/url",
                "image": "http://image.com",
                "delivery": "delivery",
                "online": True,
                "active": True,
                "is_customizable": True,
                "paid_print": True,
                "is_exclusive": True,
                "currency": "EUR",
                "url": "http://url.com",
                "attributes": '{"key": "value"}',
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data["product_id"], 1)

    def test_product_create_invalid(self):
        response = self.client.post(reverse("products:products-list"), {})
        self.assertEqual(response.status_code, 400)

    def test_product_update(self):
        product = ProductWithSingleStockFactory()
        response = self.client.patch(
            reverse("products:products-detail", args=[product.id]),
            {"name": "new name"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data["name"], "new name")

    def test_product_update_invalid(self):
        product = ProductWithSingleStockFactory()
        response = self.client.patch(
            reverse("products:products-detail", args=[product.id]),
            {"style": None},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_product_update_not_found(self):
        response = self.client.patch(
            reverse("products:products-detail", args=[1]),
            {"name": "new name"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_product_delete(self):
        product = ProductWithSingleStockFactory()
        response = self.client.delete(
            reverse("products:products-detail", args=[product.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_product_delete_not_found(self):
        response = self.client.delete(reverse("products:products-detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_product_price_info(self):
        """
        Test that the price calculations based on the tied stock are correct
        """
        product = ProductWithMultipleStock()
        price_info = product.stock.aggregate(
            min_price=Min("price"),
            max_price=Max("price"),
            reccomended_retail_price=Max("recommended_retail_price"),
            discount_percentage=Max("discount_percentage"),
        )
        price_info["currency"] = product.currency
        response = self.client.get(
            reverse("products:products-detail", args=[product.id])
        )
        self.assertDictEqual(response.data["prices"], PriceSerializer(price_info).data)
