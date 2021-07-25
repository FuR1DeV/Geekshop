from django.test import TestCase
from django.test.client import Client
from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):
    status_code_success = 200

    def setUp(self):
        cat_1 = ProductCategory.objects.create(
            name='cat 1'
        )
        Product.objects.create(
            category=cat_1,
            name='cat_1'
        )
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.status_code_success)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)
