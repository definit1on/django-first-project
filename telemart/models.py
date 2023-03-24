from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

import random

from sympy.multipledispatch.conflict import ordering

class Company(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='companies/', null=True, blank=True)
    description = models.FileField(upload_to='company_descriptions/', null=True, blank=True)
    official = models.CharField(max_length=56, null=True, blank=True)
    trailer = models.CharField(max_length=11, null=True, blank=True)
    # products

    def __str__(self):
        return self.name

    def url(self):
        return reverse('telemart:company-detail', kwargs={'pk': self.id})

    def power(self):
        products = self.products.all()
        if products:
            return sum(p.power for p in products) / len(products)
        return 0.0

    class Meta:
        ordering = ['-name']


class Product(models.Model):
    title = models.CharField(max_length=128)
    year = models.IntegerField(null=True, blank=True)
    power = models.FloatField(default=4.0)
    picture = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.FileField(upload_to='product_descriptions/', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='products')
    trailer = models.CharField(max_length=11, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    fans = models.ManyToManyField(User, related_name='product_wishlist', blank=True)
    hotline = models.CharField(max_length=56, null=True, blank=True)
    # comments

    def __str__(self):
        return self.title

    def url(self):
        return reverse('telemart:product-detail', kwargs={'slug': self.slug})


class UserAddon(models.Model):
    user = models.OneToOneField(User, related_name='addon', on_delete=models.CASCADE)
    userpic = models.ImageField(upload_to='userpics/', null=True, blank=True)

    def __str__(self):
        return f'{self.user}\' addon'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.text} ({self.product})'

    class Meta:
        ordering = ['-published']

