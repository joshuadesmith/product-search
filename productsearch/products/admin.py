from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'admin/products_changelist.html'
    save_on_top = True

    list_display = (
        'id', 'description', 'last_sold', 'department', 'price',
    )

    list_display_links = (
        'id', 'description',
    )

    list_filter = (
        'department', 'unit',
    )


admin.site.register(Product, ProductAdmin)
