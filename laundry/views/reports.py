from django.db.models import Count, Sum, Avg, Q
from datetime import date
# from weasyprint import HTML
# from django.db.models.query.RawQuerySet import raw
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.timezone import datetime, now
import time
from ..models import LaundryBill, LaundryData, Customers
from crm.models import Clients
from ..forms import LaundryBillForm, LaundryDataForm

from crm.tables import LaundryDataTable, LaundryBillTable, SumLaundryBillTable
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from django.views.generic import View
from django.template.loader import get_template
from Project.utils import render_to_pdf # for Justin code 



def canceled_bill(request):
    canceledbill = LaundryBillTable(LaundryBill.objects.filter(returns=True).order_by('-id'))
    canceledbill.paginate(page=request.GET.get("page", 1), per_page=5)
    # print(str(billtable))
    return render(request, "laundry/laundry.html", {
                                                    'returnstable':canceledbill,
                                                    })

def daily_reports(request):
    day_report = LaundryBill.objects.filter(recieveDate=date.today()) #now()
    print(day_report)
    # print(day_report)
    table = LaundryBillTable(day_report)
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    context = {
        'day_qs':day_report,
        'day_table':table,
    }
    return render(request, "laundry/laundry.html", context)


def all_remain(request): # Table for all remain bills
    remain_qs = LaundryBill.objects.filter(sumtotal__gt=0, paid__gte=0, remain__gt=0, returns=False).order_by('-id')
    # zero_qs = LaundryBill.objects.filter(sumtotal=0, paid=0, remain=0).order_by('-id')
    remain_table = LaundryBillTable(remain_qs)
    remain_table.paginate(page=request.GET.get("page", 1), per_page=5)
    
    return render(request, "laundry/laundry.html", {
                                                    'remain_qs':remain_qs,
                                                    'remain_table':remain_table,
                                                    })

                                                    
def paid_zero(request): # Table for all paid = 0 and sumtotal > 0
    zero_qs = LaundryBill.objects.filter(sumtotal__gt=0, paid=0, returns=False).order_by('-id')
    # zero_qs = LaundryBill.objects.filter(sumtotal=0, paid=0, remain=0).order_by('-id')
    zero_table = LaundryBillTable(zero_qs)
    zero_table.paginate(page=request.GET.get("page", 1), per_page=5)
    
    return render(request, "laundry/laundry.html", {
                                                    'zero_qs':zero_qs,
                                                    'zero_table':zero_table,
                                                    })


def remain_zero(request, **kwargs): # tABLE for all remain = 0 means all finished bill
    # sumtotal = kwargs.get('sumtotal')
    # sumtotal != 0
    zero_remain = LaundryBill.objects.filter(sumtotal__gt=0, returns=False, remain=0).order_by('-id')
    # zero_remain = LaundryBill.objects.raw('''SELECT * 
    #                                     FROM laundry_LaundryBill  
    #                                     WHERE sumtotal > 0 AND paid=sumtotal AND remain=0''')
    zero_remain_table = LaundryBillTable(zero_remain)
    zero_remain_table.paginate(page=request.GET.get("page", 1), per_page=5)
    table_tag = "All Finished Bills"
    
    return render(request, "laundry/laundry.html", {
                                                    'zero_remain':zero_remain,
                                                    'zero_remain_table':zero_remain_table,
                                                    'zero_remain_tag':table_tag,
                                                    })


def calculate_sum(request):
    # All Bills
    qs_1 = LaundryBill.objects.filter(returns=False).aggregate(Sum('sumtotal'), Sum('paid'), Sum('remain'))
    form_1  = LaundryBillForm(data={
                                    'sumtotal': qs_1['sumtotal__sum'],
                                    'paid': qs_1['paid__sum'],
                                    'remain': qs_1['remain__sum']
                                })
    # All Canceled Bills
    qs_2 = LaundryBill.objects.filter(returns=True).aggregate(Sum('sumtotal'), Sum('paid'), Sum('remain'))
    form_2 = LaundryBillForm(data={
                                    'sumtotal': qs_2['sumtotal__sum'],
                                    'paid': qs_2['paid__sum'],
                                    'remain': qs_2['remain__sum']
                                })
    # All Paid Bills (Finished Bills)
    qs_3= LaundryBill.objects \
                            .filter(sumtotal__gt=0, paid__gt=0, remain=0, returns=False) \
                            .aggregate(Sum('sumtotal'), Sum('paid'), Sum('remain'))
    form_3 = LaundryBillForm(data={
                                    'sumtotal': qs_3['sumtotal__sum'],
                                    'paid': qs_3['paid__sum'],
                                    'remain': qs_3['remain__sum']
                                })
    # All Remain Bills
    qs_4 = LaundryBill.objects \
                            .filter(sumtotal__gt=0, paid__gte=0, remain__gt=0, returns=False) \
                            .aggregate(Sum('sumtotal'), Sum('paid'), Sum('remain'))
    form_4 = LaundryBillForm(data={
                                    'sumtotal': qs_4['sumtotal__sum'],
                                    'paid': qs_4['paid__sum'],
                                    'remain': qs_4['remain__sum']
                                })
    context={
                'sum_form_1': form_1,
                'sum_form_2': form_2,   
                'sum_form_3': form_3,   
                'sum_form_4': form_4,   
            }
    return render(request, 'laundry/laundry_bill.html', context) 
