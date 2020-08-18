from django.urls import path
from .views import laundry_views, search, reports, pdf_files 
                    # (laundrypage,laundry_bill,newitems,additems,
                    # laundry_data,edit_bills,get_single_field,
                    # edit_items,search,delete_item,pass_data,
                    # GeneratePdf, get_pdf, export_table, 
                    # canceled_bill, paid_zero, remain_zero,
                    # calculate_sum, all_remain, daily_reports, 
                    # search_date)
# from .views import (laundrypage,laundry_bill,newitems,additems,
#                     laundry_data,edit_bills,get_single_field,
#                     edit_items,search,delete_item,pass_data,
#                     GeneratePdf, get_pdf, export_table, 
#                     canceled_bill, paid_zero, remain_zero,
#                     calculate_sum, all_remain, daily_reports, 
#                     search_date)

app_name = 'laundry'

urlpatterns = [
    path('', laundry_views.laundrypage, name='home'),
    #
    path('search/date/', search.search_date, name='search_date'),
    #
    path('day/report/', reports.daily_reports, name='daily_reports'),
    #
    path('sum/', reports.calculate_sum, name='calculate_sum'),
    #
    path('zero/paid/', reports.paid_zero, name='paid_zero'),
    #
    path('all/remain/', reports.all_remain, name='all_remain'),
    #
    path('zero/remain/', reports.remain_zero, name='remain_zero'),
    #
    path('canceled/bill/', reports.canceled_bill, name='canceled_bill'),
    #
    path('bill/', laundry_views.laundry_bill, name='bill'),
    #
    path('additem/bill=<int:bill>/', laundry_views.additems, name='additems'),
    #
    path('additem/', laundry_views.newitems, name='newitems'),
    # for add items
    path('<int:bill>/', laundry_views.laundry_data, name='data'),
    # this view was for exprement some features
    path('single/<int:bill>/', laundry_views.get_single_field, name='single_field'),
    # for edit bill (in general)
    path('bill/<int:id>/', laundry_views.edit_bills, name='edit_bills'), 
    # for edit items in every bill
    path('bill=<int:bill>/id=<int:id>/', laundry_views.edit_items, name='edit_items'), 
    #
    path('search/', search.search, name='search'), 
    #
    path('bill/<int:bill>/<int:id>/', laundry_views.delete_item, name='delete_item'), 
    # for passing data from one form to another form
    path('pass/<int:bill>/<int:customer>/<str:ltype>/<int:quantity>/<int:price>/<int:total>/',
        laundry_views.pass_data, name='pass_data'), 

    path('Gpdf/', pdf_files.GeneratePdf.as_view(), name='GeneratePdf'),
    path('pdf/', pdf_files.get_pdf, name='get_Pdf'),

    # for exporting tables2 to another format
    path('exportdata/', pdf_files.export_table, name="export_table"),
]
