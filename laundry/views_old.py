from django.db.models import Count, Sum, Avg, Q
from datetime import date
# from weasyprint import HTML
# from django.db.models.query.RawQuerySet import raw
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.timezone import datetime, now
import time
from .models import LaundryBill, LaundryData, Customers
from crm.models import Clients
from .forms import LaundryBillForm, LaundryDataForm

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
     
    # x = remain_zero(request)
    # print(x)
    # billtable = LaundryBillTable(LaundryBill.objects.all()[0:4])
    # print(str(billtable.rows[:]))
    # row_table = ", ".join(map(str, billtable.rows[0]))
    # print(", ".join(map(str, billtable.rows[0])))
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

# Create your views here.
def laundrypage(request):
    # billtable = LaundryBillTable(LaundryBill.objects.all().order_by('-id'), template_name="django_tables2/bootstrap4.html")
    billtable = LaundryBillTable(LaundryBill.objects.filter(returns=False).order_by('-id'))
    billtable.paginate(page=request.GET.get("page", 1), per_page=5)
    # canceledbill = LaundryBillTable(LaundryBill.objects.filter(returns=True).order_by('-id'))
    # canceledbill.paginate(page=request.GET.get("page", 1), per_page=3)
    # print(str(billtable))
    return render(request, "laundry/laundry.html", {
                                                    'billtable':billtable,
                                                    # 'returnstable':canceledbill,
                                                    })


def get_single_field(request, bill):
    table = LaundryDataTable(LaundryData.objects.filter(bill=bill).order_by('-id'))
    single_field = LaundryData.objects.filter(bill=bill).first()
    # query = LaundryData.objects.values('bill').annotate(dcount=Count('bill'))
    single_form = LaundryDataForm(request.POST or None, instance=single_field)
    # billfield = request.POST.get('bill')
    if single_form.is_valid():
        instance = single_form.save()
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())#('/laundry/')
    context = {
        'form':single_form,
        'single_field':single_field,
        'table':table,
    }
    return render(request, 'laundry/single_field.html', context)

def pass_data(request, bill, customer, ltype, quantity, price, total):
    table = LaundryDataTable(LaundryData.objects.filter(bill=bill).order_by('-id'))
    form = LaundryDataForm(data={
                            'bill':bill,
                            'customer':customer,
                            'launtype':ltype,
                            'quantity':quantity,
                            'price':price,
                            'total':total,
                            })
    # if form.is_valid():
    #     form.save()
        # return HttpResponseRedirect('/laundry/additem/') 
    return render(request, 'laundry/laundry.html', {'form2':form,
                                                    'table':table})

def laundry_data(request, bill, **kwargs):
    # id_bill = kwargs.get('id')
    # iditem = kwargs.get('id')
    # This for make right redirect
    addbill = LaundryBill.objects.get(id=bill)
    editbill_data = LaundryBill.objects.get(id=bill)
    print(editbill_data)
    table = LaundryDataTable(LaundryData.objects.filter(bill=bill).order_by('-id'))
    query = LaundryData.objects.filter(bill=bill).first()
    qs = LaundryData.objects.values('customer').filter(bill=bill).first()
    qs1 = LaundryData.objects.filter(bill=bill)#values('customer').filter(bill=bill).last()
    
    print(editbill_data, qs, qs1)
    # qus = LaundryData.objects.raw('SELECT customer FROM laundry_LaundryData WHERE bill=%s' % bill)
    
    customer_name = request.POST.get('customer') 
    # bill_no = request.POST.get('bill') 
    match = LaundryData.objects.filter(customer=customer_name).exists() 
    print(', m = '+ str(match))
    if qs == None: # for avoid None exception
        bound_form = LaundryDataForm(data={'bill': editbill_data, 'customer':''})
    else:
        bound_form = LaundryDataForm(data={'bill': editbill_data, 'customer':qs['customer']})
     
    if request.method == 'POST':
        form = LaundryDataForm(request.POST or None)
        # form2 = LaundryDataForm(request.POST or None)
        if form.is_valid():  
            launtype = request.POST.get('launtype')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            total = request.POST.get('total')
            customer_name = request.POST.get('customer')
            bill_no = request.POST.get('bill')
            match = LaundryData.objects.filter(customer=customer_name, bill=bill_no).exists() 
            check_bill = LaundryData.objects.filter(bill=bill).exists()
            # data = request.POST.copy()
            # newitems(request)
            pass_data(request, bill_no, customer_name, launtype, quantity, price, total)
            if check_bill: # checking for (Bill ID)   
                if match:  # editbill_data == bill and customer_name == qs['customer']
                    instance = form.save()
                    instance.save()
                    return HttpResponseRedirect(instance.get_absolute_url())#('/laundry/')
                else:
                    raise Http404('You ar trying to insert wrong Bill ID or Customer ID, '+\
                                    'Bill ID is {}'.format(str(bill))) 
                                    #' and Customer ID is {}'.format(str(qs['customer'])))
            else:
                if request.method == 'POST':
                    form = LaundryDataForm(request.POST or None)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect(reverse('laundry:data', kwargs={'bill': bill})) 
                #
                # return pass_data(request, bill_no, customer_name, launtype, quantity, price, total)
                # return HttpResponseRedirect(reverse('laundry:data', kwargs={'bill': bill}))
    else:
        form = LaundryDataForm()
        # form2 = LaundryDataForm()

    context = { 'addbill':addbill,
        'query':query,
        'editbill_data':editbill_data,
        'bound':bound_form,
        'form':form,
        'table':table,
    }
    return render(request, 'laundry/laundry.html', context)

def newitems(request, **kwargs):#, *args, **kwargs
    bill = kwargs.get('bill')
    print('additem-bill = ' + str(bill))
    table = LaundryDataTable(LaundryData.objects.filter(bill=bill).order_by('-id'))
    # qbill = LaundryData.objects.filter(bill=bill)
    newbill = LaundryBill.objects.all().last()
    bound_form = LaundryDataForm(data={'bill': newbill})
    print(LaundryBill.objects.all().last())
    if request.method == 'POST':
        # form = pass_data.form
        form = LaundryDataForm(request.POST or None)
        # launtype = request.session['launtype'] #request.POST.get('launtype')
        # quantity = request.POST.get('quantity')
        # price = request.POST.get('price')
        # total = request.POST.get('total')
        # customer_name = request.POST.get('customer')
        # bill_no = request.POST.get('bill')
        # form = LaundryDataForm(data={'launtype':launtype,
        #                             'quantity':quantity,
        #                             'price':price,
        #                             'total':total,
        #                             'customer':customer_name,
        #                             'bill':bill_no,})
        if form.is_valid():
            instance = form.save()
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())#('/laundry/')
    else:
        form = LaundryDataForm()
   
    return render(request,'laundry/laundry.html', {'form':form,
                                                   'bound':bound_form,
                                                    'table':table,
                                                    # 'form2':form2,
                                                    })


def additems(request, bill):    # this method like newitems but with an bill no  
    # bill = kwargs.get('bill')
    # print('additem-bill = ' + str(bill))
    table = LaundryDataTable(LaundryData.objects.filter(bill=bill).order_by('-id'))
    # qbill = LaundryData.objects.filter(bill=bill)
    # newbill = LaundryBill.objects.all().last()
    bound_form = LaundryDataForm(data={'bill': bill})
    print(LaundryBill.objects.all().last())
    if request.method == 'POST':
        form = LaundryDataForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())#('/laundry/')
    else:
        form = LaundryDataForm()
   
    return render(request,'laundry/laundry.html', 
                {
                    'form':form,
                    'bound':bound_form,
                    'table':table,
                    # 'form2':form2,
                })



def laundry_bill(request): # create new bill
    if request.method == 'POST':
        form = LaundryBillForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return HttpResponseRedirect('/laundry/additem/')
    else:
        form = LaundryBillForm()
    return render(request, 'laundry/laundry_bill.html',{'form':form})
        # launbill = LaundryBill(recieveDate=request.POST['recieveDate'],
        #                         endDate=request.POST['endDate'],
        #                         sumtotal=(request.POST['sumtotal']),
        #                         paid=(request.POST['paid']),
        #                         remain=(request.POST['remain'])
        #                         # client=request.POST['client']
        #                         ) #request.POST['client']
    # launbill.save()
    # return HttpResponseRedirect('/laundry/bill/')

def edit_bills(request, id, **kwargs):
    # bill = kwargs.get('bill')
    # sum_tot = LaundryData.objects.raw('''SELECT SUM(total) 
    #                                      FROM laundry_LaundryData 
    #                                      WHERE bill=%s''', [id])
    sum_tot = LaundryData.objects.filter(bill=id).aggregate(Sum('total'))
    # sum_tot1 = LaundryData.objects.filter(Q(bill__gt=id)).annotate(tot=Sum('total'))
    # sum_tot1 = LaundryData.objects.values('bill').annotate(tot=Sum('total')).order_by('-bill')
    # calc_sum = LaundryBil(sumtotal=request.POST['sumtotal'])
    query = LaundryData.objects.filter(bill=id)
    editbill = LaundryBill.objects.get(id=id) # if we use .filter() instead .get() an "_meta" error occurs
    # editbill = LaundryBill.objects.filter(Q(id__gt=id))#|Q(recieveDate__gt=kwargs.get['recieveDate'])
    form = LaundryBillForm(request.POST or None, instance=editbill)
    # form = LaundryBillForm(request.POST or None, initial={'recieveDate':editbill,
    #                                                       'endDate':editbill,
    #                                                       'sumtotal':sum_tot,
    #                                                       'paid':editbill,
    #                                                       'remain':editbill}) #editbill
    # print(sum_tot1)
    # print('bill=' + str(bill))
    print(sum_tot)
    print(editbill)
    bound_form = LaundryBillForm(data={'sumtotal': sum_tot['total__sum']}) 
    if form.is_valid():
        form.save()
        # form.fields['sumtotal'] = bound_form['sumtotal'].data
        # form.cleaned_data['sumtotal'] = bound_form['sumtotal'].value()
        return HttpResponseRedirect(editbill.get_url_by_id())
    # else:
    #     form = LaundryBillForm()
    context = {
        'form':form, 
        'bound':bound_form,
        'editbill': editbill,
        'query':query,
    }
    return render(request, 'laundry/editbills.html', context)


def edit_items(request, bill, id): # edit and update LaundryData id inside the bill
    editbill_data = LaundryBill.objects.get(id=bill) # it is here for enable me to put a button(Add items)
    table = LaundryDataTable(LaundryData.objects.filter(bill=bill).order_by('-id'))
    item_bill = LaundryData.objects.filter(bill=bill).order_by('-id') # returns all item id for this bill
    item_id = LaundryData.objects.filter(id=id).first()
    # print('item id = '+str(item_id) + ', bill= '+str(bill) + ', item bill = ' + str(item_bill) + ', QuerySet = ' + str(item_bill[1]))
    # item_id = LaundryData.objects.filter(bill=bill).first()
    qs = LaundryData.objects.values('customer').filter(bill=bill).first()
    form = LaundryDataForm(request.POST or None, instance=item_id)
    customer_name = request.POST.get('customer') 
    bill_no = request.POST.get('bill') 
    match = LaundryData.objects.filter(customer=customer_name, bill=bill_no).exists()
    # match = LaundryData.objects.filter(customer=qs['customer']).first()
    # match2 = LaundryData.objects.filter(customer=qs['customer'], bill=bill)
    # match1 = LaundryData.objects.filter(bill=bill).exist()
    # print('match1='+str(match1[0])+', match=' + str(match) + ', match2=' + str(match2[0]) +' customer=' + str(customer_name)+ '  customerNo= '+ str(qs['customer']))
    if form.is_valid():
        # bill_no = request.POST.get('bill')
        if match:      
            # print('bill= '+str(bill_no))
            instance = form.save()
            instance.save
            return HttpResponseRedirect(instance.get_url_by_bill_and_id())
        else:
            raise Http404('You ar trying to insert wrong Bill ID or Customer ID, '+\
                            'Bill ID is {}'.format(str(bill)) + \
                            ' and Customer ID is {}'.format(str(qs['customer'])))
    # else:
    #     form = LaundryDataForm()
    context = {
        'form': form,
        'table': table,
        'editbill_data':editbill_data,
        'item_bill': item_bill,
        'item_id': item_id,
    }
    return render(request, 'laundry/edit_items.html', context)
    

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

def delete_item(request, bill, id):
    del_item = LaundryData.objects.get(id=id)
    del_item.delete()
    return HttpResponseRedirect(reverse('laundry:data', kwargs={'bill':bill}))



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
