from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import Product
from .forms import AdvancedSearchForm, SearchForm, BulkUploadForm
from .filters import ProductFilterSet
from .util import validate_query_string
from .fileparse import load_products


def index(request):
    all_products = Product.objects.order_by('-last_sold')
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render({'product_list': all_products}, request))


def search(request):
    template = loader.get_template('products/search.html')
    qs = Product.objects.order_by('-last_sold')
    context = {'product_list': qs, 'form': SearchForm()}

    if request.method == 'GET':
        search_string = request.GET.get('description')
        if search_string:
            qs = qs.filter(description__icontains=search_string)
            form = SearchForm(data=request.GET)
            context['product_list'] = qs
            context['form'] = form

    return HttpResponse(template.render(context, request))


def advanced_search(request):
    try:
        validate_query_string(request)
    except RuntimeError as e:
        raise Http404(str(e.args[0]))

    template = loader.get_template('products/advsearch.html')
    qs = Product.objects.all()
    context = {'product_list': qs, 'form': AdvancedSearchForm(), 'form_error': None}

    if request.method == 'GET':
        if len(request.GET):
            try:
                form = AdvancedSearchForm(data=request.GET)
                filter_set = ProductFilterSet(request.GET)
                qs = filter_set.filter(qs)
                context['product_list'] = qs  # Necessary because filtering a queryset creates a new queryset object
                context['form'] = form
            except RuntimeError as e:
                # Lazy way of producing custom errors
                context['form_error'] = str(e.args[0])

    return HttpResponse(template.render(context, request))


@staff_member_required
def bulk_upload(request):
    if request.method == 'POST':
        # Handle the file if POST present
        num_added = load_products(request.FILES['file'])
        messages.add_message(request, messages.INFO, 'Added {} products to Database'.format(num_added))
        return HttpResponseRedirect('/admin/products/product/')
    else:
        # Load the upload page if no POST
        template = loader.get_template('products/bulkupload.html')
        form = BulkUploadForm()
        context = {'form': form}
        return HttpResponse(template.render(context, request))
