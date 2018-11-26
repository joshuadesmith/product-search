import os

from datetime import datetime
from decimal import Decimal

from .models import Product
from productsearch.settings import BASE_DIR

PRODUCTS_FILE_PATH = os.path.join(BASE_DIR, 'products.csv')

# Constants that represent the index of each column of the csv
PK = 0
DESC = 1
LAST_SOLD = 2
SHELF_LIFE = 3
DEPT = 4
PRICE = 5
UNIT = 6
XFOR = 7
COST = 8


def parse_file_line(line):
    """
    Parses a line of the products.csv file and returns a dictionary with its contents
    :return:
    """
    ret = {}

    product_attrs = line.decode('utf-8').split(',')

    # Product PK (id)
    ret['pk'] = int(product_attrs[PK].strip())

    # Product description
    ret['description'] = product_attrs[DESC].strip()

    # Product last sold date
    ret['last_sold'] = datetime.strptime(product_attrs[LAST_SOLD].strip(), "%m/%d/%Y").date()

    # Product shelf life in days
    ret['shelf_life'] = int(product_attrs[SHELF_LIFE].strip()[0])

    # Product department
    ret['department'] = product_attrs[DEPT].strip().upper()

    # Product price
    ret['price'] = Decimal(product_attrs[PRICE].strip()[1:])

    # Product unit
    ret['unit'] = product_attrs[UNIT].strip().upper()

    # Product units for price
    ret['x_for'] = int(product_attrs[XFOR].strip())

    # Product cost
    ret['cost'] = Decimal(product_attrs[COST].strip()[1:])

    return ret


def parse_products_file(file):
    """
    Parse lines of the product csv file and returns a list of dictionaries
    that represent Product objects
    :return:
    """
    product_dicts = [parse_file_line(line) for line in file]
    return product_dicts
    #
    # with open(file, 'r') as f:
    #     print('successfully opened file {}'.format(str(file)))
    #     lines = f.readlines()[1:]  # skip the first line
    #     ret = [parse_file_line(line) for line in lines]
    #
    # return ret


def load_products(file=PRODUCTS_FILE_PATH):
    """
    Create Product objects in the DB for a list of dictionaries.
    Returns the number of objects that were added to the DB.
    """
    products = parse_products_file(file)
    num_added = 0

    for p in products:
        try:
            # Check if product with id is in DB
            existing_prod = Product.objects.get(pk=p['pk'])
        except Product.DoesNotExist:
            Product.objects.create(pk=p['pk'], description=p['description'], last_sold=p['last_sold'],
                                   shelf_life=p['shelf_life'], department=p['department'], price=p['price'],
                                   unit=p['unit'], x_for=p['x_for'], cost=p['cost'])
            num_added += 1
    return num_added
