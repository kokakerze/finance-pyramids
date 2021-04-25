from django.db import models
from django.utils.timezone import now


# Create your models here.


class Currency(models.Model):
    CURRENCY_CHOICES = (
        (1, "USD"),
        (2, "EUR"),
    )

    SOURCE_CHOICES = (
        (1, "PRIVATE_BANK"),
        (2, "MONOBANK"),
        (3, "YAHOO_FINANCE"),
        (4, "VKURSE")

    )

    currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES)
    source = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)
