from django.http import HttpResponse
from django.template import loader

from .models import Product


def index(request):
    all_products = Product.objects.order_by('-last_sold')
    template = loader.get_template('products/index.html')

    return HttpResponse(template.render({'product_list': all_products}, request))


def search(request):
    # TODO
    return HttpResponse("Search view")
