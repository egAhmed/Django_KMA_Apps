from django.db import models
from django.urls import reverse
# from django.contrib.admin import widgets
# from datetime import datetime
# from django.utils import timezone
# from django.utils.timezone import now

# Create your models here.
class Registration(models.Model):

    name = models.CharField(max_length=150)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True, max_length=254)
    password = models.CharField(max_length=50)
    bio = models.TextField(blank=True)

#this class for
# class Choices(models.Model):
#       description = models.CharField(max_length=100)

class Clients(models.Model):
    # record   = models.ForeignKey(RecordFirm, on_delete=models.CASCADE)
    name       = models.CharField(max_length=200)
    phone      = models.CharField(max_length=20, blank=True, null=True)
    mobile     = models.CharField(max_length=20, blank=True, null=True)
    address    = models.CharField(max_length=200, blank=True, null=True)
    photo      = models.ImageField(upload_to='Clients_pics', blank=True)
    identityNo = models.CharField(max_length=200, blank=True, null=True)
    notes      = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name #+ " | " + str(self.photo)

    def get_absolute_url(self):
        return reverse('crm:clients_update', kwargs={'id': self.id})

    def goto_home(self):
        return reverse('crm:home')


class RecordFirm(models.Model):
    #now = timezone.now()
    Currency = (
        ('EGY', 'Egy Pound'),
        ('USD', 'US Dollar')
    )

    # Tax_Choice = ('taxno', 'Tax No.')
    # Part_Choice=('partno', 'Part No.')
    # Purchase_Choice=('purchaseno', 'Purchase No.')
    client_id   = models.ForeignKey(Clients,
                                    on_delete=models.CASCADE,
                                    default=False,
                                    null=False)
    firm_name   = models.CharField(max_length=200,
                                blank=True,
                                null=True,
                                name='Company Name')  # name= 'Company Name'
    manager     = models.CharField(max_length=200, blank=True, null=True)
    repres_name = models.CharField(max_length=200, blank=True, null=True)
    last_visit  = models.DateField()
    notes       = models.TextField()
    type        = models.CharField(max_length=3, choices=Currency, null=True)
    #paper       = models.ManyToManyField(Choices)
    tax_no      = models.BooleanField(default=False)
    part_no     = models.BooleanField(default=False)
    purchase_no = models.BooleanField(default=False)
    # client_id   = models.

    def __str__(self):
        return self.client_id

    def get_url(self):
        return reverse('crm:firm_update', kwargs={'id': self.id})

    def go_home(self):
        return reverse('crm:regdata') # , kwargs={'id': self.id}
