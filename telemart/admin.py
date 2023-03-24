from django.contrib import admin

from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', 'year')}
    list_display = ['title', 'company', 'year', 'power']
    list_filter = ['company', 'year', 'power']


@admin.register(UserAddon)
class UserAddonAdmin(admin.ModelAdmin):
    pass

