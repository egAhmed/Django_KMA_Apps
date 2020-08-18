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






def search_date(request):
    laundry_search_from = request.GET.get('f')
    laundry_search_to = request.GET.get('t')
    if laundry_search_from:
        date_search = LaundryBill.objects.filter(Q(recieveDate__range=[laundry_search_from, laundry_search_to])).order_by('-id')
        date_table_search =  LaundryBillTable(date_search)
        date_table_search.paginate(page=request.GET.get("page", 1), per_page=5)
    elif laundry_search_to:
        date_search = LaundryBill.objects.filter(Q(recieveDate__range=[laundry_search_from, laundry_search_to])).order_by('-id')
        date_table_search =  LaundryBillTable(date_search)
        date_table_search.paginate(page=request.GET.get("page", 1), per_page=5)
    elif (laundry_search_from) or (laundry_search_to) == '':
        return HttpResponseRedirect('/laundry/')
    else:
        date_search = LaundryBill.objects.all().order_by('-id')
    
    context={ 
            'date_table_search':date_table_search,
            }
    return render(request, 'laundry/laundry.html', context)


def search(request):
    laundry_search = request.GET.get('q')
    # laundry_search_from = request.GET.get('f')
    # laundry_search_to = request.GET.get('t')
    
    if (laundry_search).isnumeric():
        results_id = LaundryBill.objects.filter(Q(id=laundry_search))#.order_by('-id')
        table_search =  LaundryBillTable(results_id)
        # table_search.paginate(page=request.GET.get("page", 1), per_page=15)
    # elif(laundry_search).isnumeric() = None:
    #     pass
    elif laundry_search:
        results_user = LaundryBill.objects.filter(
                          Q(client_id__name__icontains=laundry_search)\
                        | Q(recieveDate__icontains=laundry_search)\
                        | Q(endDate__icontains=laundry_search)).order_by('-id') 
        table_search =  LaundryBillTable(results_user)
        table_search.paginate(page=request.GET.get("page", 1), per_page=15)
    elif (laundry_search) == '':
        return HttpResponseRedirect('/laundry/')
    # elif laundry_search_from:
    #     date_search = LaundryBill.objects.filter(Q(recieveDate__range=[laundry_search_from, laundry_search_to]))
    #     date_table_search =  LaundryBillTable(date_search)
    #     date_table_search.paginate(page=request.GET.get("page", 1), per_page=5)
    # elif (laundry_search_from) or (laundry_search_to) == '':
    #     return HttpResponseRedirect('/laundry/')
    else:
        results_user = LaundryBill.objects.all().order_by('-id')
        # date_search = LaundryBill.objects.all().order_by('-id')

    # if laundry_search_from:
    #     date_search = LaundryBill.objects.filter(Q(recieveDate__range=[laundry_search_from, laundry_search_to]))
    #     date_table_search =  LaundryBillTable(date_search)
    #     date_table_search.paginate(page=request.GET.get("page", 1), per_page=5)
    # elif (laundry_search_from) or (laundry_search_to) == '':
    #     return HttpResponseRedirect('/laundry/')
    # else:
    #     date_search = LaundryBill.objects.all().order_by('-id')

    context={ 
            'table_search':table_search,
            # 'date_table_search':date_table_search,
            }
    return render(request, 'laundry/laundry.html', context)
