from django.db import models


class Product(models.Model):
    # Department Constants
    GROCERY = "GROCERY"
    PRODUCE = "PRODUCE"
    PHARMACY = "PHARMACY"

    # Department Choice Field Options
    DEPARTMENT_CHOICES = (
        (GROCERY, "Grocery"),
        (PRODUCE, "Produce"),
        (PHARMACY, "Pharmacy"),
    )

    # Unit Constants
    LB = "LB"
    EACH = "EACH"

    # Unit Choice Field Options
    UNIT_CHOICES = (
        (LB, "lb"),
        (EACH, "each"),
    )

    description = models.CharField(max_length=200)

    last_sold = models.DateField()

    shelf_life = models.IntegerField()

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    price = models.DecimalField(decimal_places=2, max_digits=6)

    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    x_for = models.IntegerField()

    cost = models.DecimalField(decimal_places=2, max_digits=6)
