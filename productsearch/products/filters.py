import re

from django import forms
from datetime import datetime
from decimal import Decimal


EMPTY_VALUES = {
    0,
    None,
    '',
    'None',
    'N/A',
}


class CustomFilter(object):
    field_class = forms.Field

    def __init__(self, field_name=None, lookup_expression='icontains', **kwargs):
        self.field_name = field_name
        self.lookup_expression = lookup_expression

    def get_method(self, qs):
        """
        Return our desired filter method.

        This currently isn't necessary but would allow for other kinds of query operations
        such as exclude() or distinct()
        """
        return qs.filter

    def filter(self, qs, val):
        """
        Filter a queryset based on this CustomFilter's parameters, a given
        QuerySet, and a given value.
        """
        if not self.field_name or val in EMPTY_VALUES:
            return qs

        lookup = '{}__{}'.format(self.field_name, self.lookup_expression)
        qs = self.get_method(qs)(**{lookup: val})

        return qs


LOOKUP_EXPRESSIONS = {
    'description': 'icontains',
    'department': 'icontains',
    'last_sold_min': 'gte',
    'last_sold_max': 'lte',
    'shelf_life_min': 'gte',
    'shelf_life_max': 'lte',
    'price_min': 'gte',
    'price_max': 'lte',
    'cost_min': 'gte',
    'cost_max': 'lte',
    'unit': 'iexact',
    'x_for': 'exact',
}


FIELD_TYPES = {
    'description': forms.CharField,
    'department': forms.CharField,
    'last_sold_min': forms.DateField,
    'last_sold_max': forms.DateField,
    'shelf_life_min': forms.IntegerField,
    'shelf_life_max': forms.IntegerField,
    'price_min': forms.DecimalField,
    'price_max': forms.DecimalField,
    'cost_min': forms.DecimalField,
    'cost_max': forms.DecimalField,
    'unit': forms.CharField,
    'x_for': forms.IntegerField,
}


class ProductFilterSet(object):

    def __init__(self, data=None):
        self.filters = []
        self.data = data

    def filter(self, qs):
        if not self.data:
            return qs

        for field_name, val in self.data.items():
            if val not in EMPTY_VALUES:
                val = self.convert_value(field_name, val)
                qs = self.custom_filter(field_name).filter(qs, val)

        return qs

    def convert_value(self, field_name, value):
        field_type = FIELD_TYPES[field_name]
        value = value.strip()

        if field_type == forms.DateField:
            return datetime.strptime(value, "%m/%d/%Y")

        if field_type == forms.DecimalField:
            if not value.isdigit():
                value = re.findall(r'[-+]?\d*\.\d+|\d+', value)[0]  # Clean decimal number
            return Decimal(value)

        if field_type == forms.IntegerField:
            if not value.isdigit():
                regex = re.compile('[^0-9]')  # Get rid of non numeric characters
                value = re.sub(regex, '', value)
            return int(value)

        return value

    def custom_filter(self, field_name):
        if 'min' in field_name or 'max' in field_name:  # Handle form fields that don't match field names
            expr = LOOKUP_EXPRESSIONS[field_name]
            field = field_name.rsplit('_', 1)[0]
            return CustomFilter(field_name=field, lookup_expression=expr)
        return CustomFilter(field_name=field_name, lookup_expression=LOOKUP_EXPRESSIONS[field_name])
