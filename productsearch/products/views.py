from django.http import HttpResponse
from django.template import loader

from .models import Product


def index(request):
    all_products = Product.objects.order_by('-last_sold')
    template = loader.get_template('products/index.html')

    return HttpResponse(template.render({'product_list': all_products}, request))


def search(request):
    qs = Product.objects.order_by('-last_sold')
    if request.method == 'GET':
        search_string = request.GET.get('search_text')
        if search_string:
            qs = qs.filter(description__icontains=search_string)

    template = loader.get_template('products/index.html')

    return HttpResponse(template.render({'product_list': qs}, request))


def advanced_search(request):
    qs = Product.objects.order_by('-last_sold')
    if request.method == 'GET':
        print(request.GET)
        desc = request.GET.get('description')
        dep = request.GET.get('department')

        if desc:
            qs = qs.filter(description__icontains=desc)

        if dep:
            qs = qs.filter(department__icontains=dep)

    template = loader.get_template('products/advsearch.html')

    return HttpResponse(template.render({'product_list': qs}, request))
