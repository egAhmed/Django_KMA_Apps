from django.db import models
from django.urls import reverse
from crm.models import Clients
from django.utils.timezone import timezone
from datetime import date
# from timezone import now

# Create your models here.
class Customers(models.Model):
    customerName = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return "{}".format(self.customerName)

class LaundryBill(models.Model):
    recieveDate  = models.DateField(default=date.today, null=True)
    endDate      = models.DateField(default=date.today, null=True)
    sumtotal     = models.FloatField(default=00.00, null=True)
    paid         = models.FloatField(default=00.00, null=True)
    remain       = models.FloatField(default=00.00, null=True)
    paidDone     = models.BooleanField(default=False)
    returns      = models.BooleanField(default=False)
    stillremain  = models.BooleanField(default=False)
    remaindone   = models.BooleanField(default=False)
    closebill    = models.BooleanField(default=False)
    client       = models.ForeignKey(Clients, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.id)

    def get_url_by_id(self):
        return reverse('laundry:edit_bills', kwargs={'id':self.id})
    
    # def get_url_for_calculations(self):
    #     return reverse('laundry:calculations', kwargs={
    #                                                     'sumtotal':self.sumtotal,
    #                                                     'paid':self.paid,
    #                                                     'remain':self.remain
    #                                                     })


class LaundryData(models.Model):
    launtype  = models.CharField(max_length=100, null=True)
    quantity  = models.IntegerField(blank=True, null=True)
    price     = models.FloatField(default=00.00, null=True)
    total     = models.FloatField(default=00.00, null=True)
    customer  = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bill      = models.ForeignKey(LaundryBill, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.id)
    
    def get_absolute_url(self):
        return reverse('laundry:data', kwargs={'bill': self.bill})

    def get_url_by_bill_and_id(self):
        return reverse("laundry:edit_items", 
                        kwargs={'bill': self.bill,
                                'id': self.id
                        })

    def get_url_for_pass_data(self):
        return reverse('laundry:pass_data',
                        kwargs={'bill':self.bill,
                                'customer':self.customer,
                                'launtype':self.launtype,
                                'quantity':self.quantity,
                                'price':self.price,
                                'total':self.total,})

# class HandleBill(models.Model):

          