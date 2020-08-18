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


def delete_item(request, bill, id):
    del_item = LaundryData.objects.get(id=id)
    del_item.delete()
    return HttpResponseRedirect(reverse('laundry:data', kwargs={'bill':bill}))

