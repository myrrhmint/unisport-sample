from django.test import TestCase
from django.urls import reverse

from products.models import Label
from products.serializers import (
    LabelSerializer,
    ProductLabelSerializer,
)
from products.tests.factories.products import LabelFactory, ProductFactory


class LabelTestCase(TestCase):
    def test_label_list(self):
        [LabelFactory() for _ in range(10)]
        expected_labels = Label.objects.all()
        response = self.client.get(reverse("products:labels-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertListEqual(
            [label["id"] for label in response.data["results"]],
            [label.id for label in expected_labels],
        )

    def test_label_list_no_result(self):
        response = self.client.get(reverse("products:labels-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], [])

    def test_label_detail(self):
        label = LabelFactory()
        response = self.client.get(reverse("products:labels-detail", args=[label.id]))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, LabelSerializer(label).data)

    def test_label_detail_not_found(self):
        response = self.client.get(reverse("products:labels-detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_label_create(self):
        label = LabelFactory.stub().__dict__
        response = self.client.post(reverse("products:labels-list"), label)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.data,
            LabelSerializer(Label.objects.get(pk=response.data["id"])).data,
        )

    def test_label_create_invalid_data(self):
        label = LabelFactory.stub().__dict__
        label["name"] = ""
        response = self.client.post(reverse("products:labels-list"), label)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Label.objects.count(), 0)

    def test_label_update(self):
        label = LabelFactory()
        response = self.client.patch(
            reverse("products:labels-detail", args=[label.id]),
            {"name": "new name"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.get(pk=label.id).name, "new name")

    def test_label_update_invalid_data(self):
        label = LabelFactory()
        response = self.client.patch(
            reverse("products:labels-detail", args=[label.id]),
            {"name": ""},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Label.objects.get(pk=label.id).name, label.name)

    def test_label_delete(self):
        label = LabelFactory()
        response = self.client.delete(
            reverse("products:labels-detail", args=[label.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Label.objects.count(), 0)


class ProductLabelTestcase(TestCase):
    def test_label_list_from_product(self):
        """
        Test that a label can be retrieved from the tied product
        """
        product = ProductFactory()
        label = LabelFactory()
        product.labels.add(label)
        response = self.client.get(
            reverse("products:product-labels-list", args=[product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data["results"][0], ProductLabelSerializer(label).data
        )

    def test_label_list_from_product_not_found(self):
        response = self.client.get(reverse("products:product-labels-list", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_label_create_with_product(self):
        """
        Test that a label can be tied to a product
        """
        product = ProductFactory()
        label = LabelFactory()
        response = self.client.post(
            reverse("products:product-labels-list", args=[product.id]),
            {"label_id": label.id},
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.data,
            ProductLabelSerializer(
                Label.objects.get(pk=response.data["label_id"])
            ).data,
        )
        self.assertEqual(product.labels.count(), 1)
        self.assertEqual(product.labels.first().id, response.data["label_id"])

    def test_label_create_with_product_not_found(self):
        response = self.client.post(
            reverse("products:product-labels-list", args=[1111]), {"label_id": 1}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Label.objects.count(), 0)

    def test_label_create_with_product_invalid_data(self):
        product = ProductFactory()
        response = self.client.post(
            reverse("products:product-labels-list", args=[product.id]), {"name": "test"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(product.labels.count(), 0)
        self.assertEqual(Label.objects.count(), 0)

    def test_delete_label_with_tied_product(self):
        """
        Test that a label can be removed from a product
        """
        product = ProductFactory()
        label = LabelFactory()
        product.labels.add(label)
        response = self.client.delete(
            reverse("products:labels-detail", args=[label.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(product.labels.count(), 0)
        self.assertEqual(Label.objects.count(), 0)

    def test_delete_label_with_tied_product_not_found(self):
        response = self.client.delete(reverse("products:labels-detail", args=[1]))
        self.assertEqual(response.status_code, 404)
