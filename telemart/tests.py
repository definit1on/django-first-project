from django.test import TestCase

from .models import *

class CompanyModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name='Logitech')

    def test1(self):
        company = Company.objects.get(id__exact=1)
        s1 = company.name
        s2 = str(company)
        self.assertEqual(s1, s2)


class CompanyListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        n=5
        for i in range(n):
            Company.objects.create(name=f'Smth{i}', icon='10400f.jpg')

    def test1(self):
        resp = self.client.get(reverse('telemart:company-list'))
        self.assertEqual(resp.status_code, 200)

    def test2(self):
        resp = self.client.get(reverse('telemart:company-list'))
        self.assertTemplateUsed(resp, 'telemart/company_list.html')

    def test3(self):
        company = Company.objects.get(id__exact=1)
        self.assertEqual(len(company.products.all()), 0)

    def test4(self):
        company = Company.objects.get(id__exact=1)
        self.assertEqual(company.power(), 0.0)

    def test5(self):
        company = Company.objects.get(id__exact=1)
        self.assertEqual(company.trailer, None)

    def test6(self):
        company = Company.objects.get(id__exact=1)
        ml = company._meta.get_field('official').max_length
        self.assertEqual(ml, 56)


class ProductListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        n = 5
        for i in range(n):
            Product.objects.create(title=f'Smth{i}', picture='10400f.jpg')

    def test1(self):
        resp = self.client.get(reverse('telemart:product-list'))
        self.assertEqual(resp.status_code, 200)

    def test2(self):
        resp = self.client.get(reverse('telemart:product-list'))
        self.assertTemplateUsed(resp, 'telemart/product_list.html')

    def test3(self):
        product = Product.objects.get(id__exact=1)
        self.assertEqual(product.power, 4.0)

    def test4(self):
        product = Product.objects.get(id__exact=1)
        ml = product._meta.get_field('title').max_length
        self.assertEqual(ml, 128)

    def test5(self):
        product = Product.objects.get(id__exact=1)
        self.assertEqual(product.company, None)

    def test6(self):
        product = Product.objects.get(id__exact=1)
        s1 = product.title
        s2 = str(product)
        self.assertEqual(s1, s2)

    def test7(self):
        product = Product.objects.get(id__exact=1)
        self.assertEqual(len(product.comments.all()), 0)
