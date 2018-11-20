from django.http import HttpResponse
from django.template import loader

from .models import Product
from .forms import AdvancedSearchForm, SearchForm
from .filters import ProductFilterSet


def index(request):
    print('In index view')
    all_products = Product.objects.order_by('-last_sold')
    template = loader.get_template('products/index.html')

    return HttpResponse(template.render({'product_list': all_products}, request))


def search(request):
    print('In search view')
    template = loader.get_template('products/index.html')
    qs = Product.objects.order_by('-last_sold')
    if request.method == 'GET':
        search_string = request.GET.get('description')
        if search_string:
            qs = qs.filter(description__icontains=search_string)
            form = SearchForm(data=request.GET)
            return HttpResponse(template.render({'product_list': qs, 'form': form}, request))

    return HttpResponse(template.render({'product_list': qs, 'form': SearchForm()}, request))


def advanced_search(request):
    print('In advanced_search view')
    template = loader.get_template('products/advsearch.html')
    qs = Product.objects.all()
    if request.method == 'GET':
        print('In advanced_search.GET block')
        if len(request.GET):
            form = AdvancedSearchForm(data=request.GET)
            filter_set = ProductFilterSet(request.GET)
            qs = filter_set.filter(qs)
            return HttpResponse(template.render({'product_list': qs, 'form': form}, request))

    print('Not in advanced_search.GET block')
    return HttpResponse(template.render({'product_list': qs, 'form': AdvancedSearchForm()}, request))
