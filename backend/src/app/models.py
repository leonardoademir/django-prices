from django.db import models
from django.core.validators import MaxLengthValidator

class PriceModel(models.Model):

    currency = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        validators=[MaxLengthValidator(3)]
    )

    date = models.DateField(null=False)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'price'
