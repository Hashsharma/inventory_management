from django.contrib import admin

from inventory.models import Product, Category


# Register your models here.

#
# class ZoneFileAdmin(admin.ModelAdmin):
#     list_display = ['zone_name', 'zone_id']
#     list_filter = ['zone_name']
#     search_fields = ['zone_name', 'zone_id']
#
# admin.site.register(ZoneFiles, ZoneFileAdmin)
#

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_desc', 'category', 'product_quantity_in_stock', 'product_price']
    list_filter = ['product_name']

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

admin.site.register(Category, CategoryAdmin)