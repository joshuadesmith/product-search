from django.test import TestCase
from datetime import date
from decimal import Decimal

from .models import Product
from .filters import CustomFilter, EMPTY_VALUES, LOOKUP_EXPRESSIONS, ProductFilterSet


class CustomFilterTests(TestCase):

    def setUp(self):
        super().setUp()
        self.qs = Product.objects.all()
        self.custom_filter = CustomFilter(field_name='description')
        # Make sure initial_obj_count matches the number of objects created
        # in this method
        self.initial_obj_count = 2

        Product.objects.create(description='Apple',
                               last_sold=date.today(),
                               shelf_life=1,
                               department=Product.PRODUCE,
                               price=Decimal("2.99"),
                               unit=Product.LB,
                               x_for=1,
                               cost=Decimal("1.55"))
        Product.objects.create(description='Banana',
                               last_sold=date.today(),
                               shelf_life=1,
                               department=Product.PRODUCE,
                               price=Decimal("1.99"),
                               unit=Product.LB,
                               x_for=1,
                               cost=Decimal("0.55"))

    def test_get_method_filter(self):
        """
        Test that the default filter method is qs.filter
        """
        method = self.custom_filter.get_method(self.qs)
        self.assertEqual(method.__name__, 'filter')

    def test_custom_filter_empty_val(self):
        """
        Test that a queryset is unmodified when filtered against 'empty' values
        """
        sql_query = self.qs.query.__str__
        for val in EMPTY_VALUES:
            self.assertEqual(self.custom_filter.filter(self.qs, val).query.__str__, sql_query)

    def test_custom_filter_consistency(self):
        """
        Test that using the CustomFilter.filter method returns a QuerySet that
        performs the same SQL operation as QuerySet.filter
        """
        self.assertEqual(len(self.qs), self.initial_obj_count)  # Might be a bit over the top

        filtered_qs = self.qs.filter(description__icontains='apple')
        custom_filtered_qs = self.custom_filter.filter(self.qs, 'apple')

        # Compare the generated SQL strings from each queryset
        self.assertEqual(str(filtered_qs.query), str(custom_filtered_qs.query))


class ProductFilterSetTests(TestCase):
    def setUp(self):
        super().setUp()
        self.qs = Product.objects.all()
        # Initial Objects:
        Product.objects.create(description='Apple',
                               last_sold=date.today(),
                               shelf_life=1,
                               department=Product.PRODUCE,
                               price=Decimal("2.99"),
                               unit=Product.LB,
                               x_for=1,
                               cost=Decimal("1.55"))
        Product.objects.create(description='Cold and Flu Medicine',
                               last_sold=date.today(),
                               shelf_life=1,
                               department=Product.PHARMACY,
                               price=Decimal("8.99"),
                               unit=Product.LB,
                               x_for=1,
                               cost=Decimal("4.55"))
        Product.objects.create(description='Milk',
                               last_sold=date.today(),
                               shelf_life=1,
                               department=Product.GROCERY,
                               price=Decimal("3.99"),
                               unit=Product.LB,
                               x_for=1,
                               cost=Decimal("1.55"))

    def test_convert_value_date(self):
        """
        Test that ProductFilterSet.convert_value converts formatted strings to date objects
        """
        fs = ProductFilterSet()
        date_str = '12/21/1993'
        converted_date = fs.convert_value('last_sold_max', date_str)
        self.assertIsInstance(converted_date, date)
        self.assertEqual(converted_date.day, 21)
        self.assertEqual(converted_date.month, 12)
        self.assertEqual(converted_date.year, 1993)

    def test_convert_value_decimal(self):
        """
        Test that ProductFilterSet.convert_value converts formatted strings to Decimal objects
        """
        fs = ProductFilterSet()
        conv_dec = fs.convert_value('price_max', '$1.99')
        self.assertIsInstance(conv_dec, Decimal)
        self.assertEqual(conv_dec, Decimal('1.99'))

    def test_convert_value_integer(self):
        """
        Test that ProductFilterSet.convert_value converts formatted strings to ints
        """
        fs = ProductFilterSet()
        conv_int = fs.convert_value('shelf_life_max', '4d')
        self.assertIsInstance(conv_int, int)
        self.assertEqual(conv_int, 4)

    def test_custom_filter(self):
        """
        Test that the ProductFilterSet.custom_filter returns correct CustomFilter objects
        for each advanced search field
        """
        fs = ProductFilterSet()
        cf = fs.custom_filter('id_num')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'id')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['id_num'])

        cf = fs.custom_filter('description')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'description')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['description'])

        cf = fs.custom_filter('department')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'department')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['department'])

        cf = fs.custom_filter('last_sold_max')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'last_sold')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['last_sold_max'])

        cf = fs.custom_filter('last_sold_min')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'last_sold')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['last_sold_min'])

        cf = fs.custom_filter('shelf_life_min')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'shelf_life')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['shelf_life_min'])

        cf = fs.custom_filter('shelf_life_max')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'shelf_life')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['shelf_life_max'])

        cf = fs.custom_filter('price_min')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'price')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['price_min'])

        cf = fs.custom_filter('price_max')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'price')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['price_max'])

        cf = fs.custom_filter('cost_min')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'cost')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['cost_min'])

        cf = fs.custom_filter('cost_max')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'cost')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['cost_max'])

        cf = fs.custom_filter('unit')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'unit')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['unit'])

        cf = fs.custom_filter('x_for')
        self.assertIsInstance(cf, CustomFilter)
        self.assertEqual(cf.field_name, 'x_for')
        self.assertEqual(cf.lookup_expression, LOOKUP_EXPRESSIONS['x_for'])

    def test_filter(self):
        """
        Test that ProductFilterSet.filter works (happy path)
        """
        fs = ProductFilterSet(data={'description': 'apple'})
        filtered_qs = fs.filter(self.qs)
        for product in filtered_qs:
            self.assertTrue('apple' in product.description.lower())
