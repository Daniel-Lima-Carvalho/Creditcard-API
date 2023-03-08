from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Creditcard(models.Model):
    exp_date = models.DateTimeField(verbose_name=_('expiration date'))
    holder = models.CharField(max_length=500, verbose_name=_('holder'))
    number = models.CharField(max_length=500, verbose_name=_('number'))
    cvv = models.IntegerField(verbose_name=_('cvv'))

    def __str__(self):
        return f'{self.number} - {self.holder}'