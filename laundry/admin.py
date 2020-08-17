from django.contrib import admin
from .models import LaundryBill, LaundryData, Customers

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id',]

class LaundryBillAdmin(admin.ModelAdmin):
    """docstring for LaundryAdmin."""
    list_display = ['id', 'recieveDate', 'endDate',
                    'sumtotal', 'paid', 'remain']
    
class LaundryDataAdmin(admin.ModelAdmin):
    list_display = ['bill', 'customer', 'launtype',
                    'quantity', 'price', 'total']


admin.site.register(LaundryBill, LaundryBillAdmin)
admin.site.register(LaundryData, LaundryDataAdmin)
admin.site.register(Customers, CustomerAdmin)
