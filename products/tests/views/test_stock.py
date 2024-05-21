from django.test import TestCase
from django.urls import reverse

from products.models import Stock
from products.serializers import StockSerializer
from products.tests.factories.products import (
    ProductFactory,
    ProductWithMultipleStock,
    ProductWithSingleStockFactory,
    StockFactory,
)


class StockTestCase(TestCase):
    def test_result_single_stock(self):
        product = ProductWithSingleStockFactory()
        response = self.client.get(
            reverse("products:product-stock-list", args=[product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertListEqual(
            [stock["id"] for stock in response.data["results"]],
            [stock.id for stock in product.stock.all()],
        )

    def test_result_multiple_stock(self):
        """
        Test that the stock list for a specific product returns its stock ordered by size
        """
        product = ProductWithMultipleStock()
        expected_stock_total = Stock.objects.filter(product=product).order_by("size_id")
        response = self.client.get(
            reverse("products:product-stock-list", args=[product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            [stock["id"] for stock in response.data["results"]],
            [stock.id for stock in expected_stock_total],
        )

    def test_stock_list_product_not_found(self):
        response = self.client.get(reverse("products:product-stock-list", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_stock_detail_not_found(self):
        response = self.client.get(
            reverse("products:product-stock-detail", args=[1, 1])
        )
        self.assertEqual(response.status_code, 404)

    def test_stock_detail(self):
        stock = StockFactory()
        response = self.client.get(
            reverse("products:product-stock-detail", args=[stock.product.id, stock.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, StockSerializer(stock).data)

    def test_stock_create(self):
        product = ProductFactory()
        stock = StockFactory.stub().__dict__
        del stock["product"]
        response = self.client.post(
            reverse("products:product-stock-list", args=[product.id]), stock
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, StockSerializer(Stock.objects.first()).data)
        self.assertEqual(product.stock.count(), 1)
        self.assertEqual(product.stock.first().id, response.data["id"])

    def test_stock_create_invalid(self):
        product = ProductFactory()
        response = self.client.post(
            reverse("products:product-stock-list", args=[product.id]), {}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Stock.objects.count(), 0)

    def test_stock_update(self):
        stock = StockFactory()
        response = self.client.patch(
            reverse(
                "products:product-stock-detail",
                args=[stock.product.id, stock.id],
            ),
            {"barcode": "new-barcode"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        stock.refresh_from_db()
        self.assertEqual(stock.barcode, "new-barcode")

    def test_stock_update_invalid(self):
        stock = StockFactory()
        response = self.client.patch(
            reverse(
                "products:product-stock-detail",
                args=[stock.product.id, stock.id],
            ),
            {"barcode": None},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        stock.refresh_from_db()

    def test_stock_delete(self):
        stock = StockFactory()
        response = self.client.delete(
            reverse(
                "products:product-stock-detail",
                args=[stock.product.id, stock.id],
            )
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Stock.objects.count(), 0)

    def test_stock_delete_not_found(self):
        response = self.client.delete(
            reverse("products:product-stock-detail", args=[1, 1])
        )
        self.assertEqual(response.status_code, 404)
