from django.urls import path
from .views import (laundrypage,laundry_bill,newitems,additems,
                    laundry_data,edit_bills,get_single_field,
                    edit_items,search,delete_item,pass_data,
                    GeneratePdf, get_pdf, export_table, 
                    canceled_bill, paid_zero, remain_zero,
                    calculate_sum, all_remain, daily_reports, 
                    search_date)

app_name = 'laundry'

urlpatterns = [
    path('', laundrypage, name='home'),
    #
    path('search/date/', search_date, name='search_date'),
    #
    path('day/report/', daily_reports, name='daily_reports'),
    #
    path('sum/', calculate_sum, name='calculate_sum'),
    #
    path('zero/paid/', paid_zero, name='paid_zero'),
    #
    path('all/remain/', all_remain, name='all_remain'),
    #
    path('zero/remain/', remain_zero, name='remain_zero'),
    #
    path('canceled/bill/', canceled_bill, name='canceled_bill'),
    #
    path('bill/', laundry_bill, name='bill'),
    #
    path('additem/bill=<int:bill>/', additems, name='additems'),
    #
    path('additem/', newitems, name='newitems'),
    # for add items
    path('<int:bill>/', laundry_data, name='data'),
    # this view was for exprement some features
    path('single/<int:bill>/', get_single_field, name='single_field'),
    # for edit bill (in general)
    path('bill/<int:id>/', edit_bills, name='edit_bills'), 
    # for edit items in every bill
    path('bill=<int:bill>/id=<int:id>/', edit_items, name='edit_items'), 
    #
    path('search/', search, name='search'), 
    #
    path('bill/<int:bill>/<int:id>/', delete_item, name='delete_item'), 
    # for passing data from one form to another form
    path('pass/<int:bill>/<int:customer>/<str:ltype>/<int:quantity>/<int:price>/<int:total>/', pass_data, name='pass_data'), 

    path('Gpdf/', GeneratePdf.as_view(), name='GeneratePdf'),
    path('pdf/', get_pdf, name='get_Pdf'),

    # for exporting tables2 to another format
    path('exportdata/', export_table, name="export_table"),
]
