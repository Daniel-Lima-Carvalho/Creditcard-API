from django.contrib import admin
from creditcard.models import Creditcard

@admin.register(Creditcard)
class CreditcardAdmin(admin.ModelAdmin):
    fields = ('exp_date', 'holder', 'number', 'cvv')
    readonly_fields = ('exp_date', 'holder', 'number', 'cvv')
    search_fields = ('exp_date', 'holder', 'number', 'cvv')
    list_display = ('exp_date', 'holder', 'number', 'cvv')