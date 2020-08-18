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

#################################################################


# Justin code to render html to pdf
class GeneratePdf(View):
    # def get(self, request, *args, **kwargs):
    #     billtable = LaundryBillTable(LaundryBill.objects.all().order_by('-id'))
    #     template = get_template('laundry/pdf.html')
    #     context = {
    #         "billtable":billtable,
    #         "invoice_id": 123,
    #         "customer_name": "John Cooper",
    #         "amount": 1399.99,
    #         "today": "Today",
    #     }
    #     html = template.render(context)
    #     pdf = render_to_pdf('laundry/pdf.html', context)
    #     if pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         filename = "Invoice_%s.pdf" %("12341231")
    #         content = "inline; filename='%s'" %(filename)
    #         download = request.GET.get("download")
    #         if download:
    #             content = "attachment; filename='%s'" %(filename)
    #         response['Content-Disposition'] = content
    #         return response
    #     return HttpResponse(pdf, content_type='application/pdf')

    def get(self, request, *args, **kwargs):
        zero_remain = LaundryBill.objects.filter(sumtotal__gt=0, returns=False, remain=0).order_by('-id')
        template = get_template('laundry/zero_remain.html')
        context = {
            "zero_remain":zero_remain,
        }
        html = template.render(context)
        pdf = render_to_pdf('laundry/zero_remain.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse(pdf, content_type='application/pdf')


#This is func based to render to pdf
def get_pdf(request, *args, **kwargs):
    # table = LaundryBillTable(LaundryBill.objects.all().order_by('-id'))
    # table.paginate(page=request.GET.get("page", 1), per_page=15)
    query = LaundryBill.objects.all().order_by('-id')
    zero_remain = LaundryBill.objects.filter(sumtotal__gt=0, returns=False, remain=0).order_by('-id')
    template = get_template('laundry/pdf.html')
    context = {'zero_remain':zero_remain,
        "query":query,
        "invoice_id": 123,
        "customer_name": "John Cooper",
        "amount": 1399.99,
        "today": "Today",
    }
    html = template.render(context)
    pdf = render_to_pdf('laundry/pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_"+str(time.strftime('%d-%m-%Y'))+".pdf" #%('%Y-%m-%d')
        content = "inline; filename=%s" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse(pdf, content_type='application/pdf')


# Export to any kind of document from tables2_Documentation
def export_table(request):
    table = LaundryBillTable(LaundryBill.objects.all().order_by('-id'))
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, "laundry/export_table.html", {"table": table})
