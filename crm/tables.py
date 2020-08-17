import django_tables2 as tables
from django.db.models import Sum
from .models import Clients
from laundry.models import LaundryData, LaundryBill


class ClientsTable(tables.Table):
    class Meta:
        model         = Clients
        template_name = "django_tables2/bootstrap.html"
        fields        = ('name','phone','mobile','address','identityNo',)

class LaundryDataTable(tables.Table):
    ''' Here is the solution to make the table items clickable 
    https://stackoverflow.com/questions/44911679/putting-a-click-event-for-a-dialogue-box-with-django-tables2
    '''
    bill = tables.TemplateColumn('<a href="/laundry/bill/{{ record.bill }}/">{{ record.bill }}</a>',
                                verbose_name=u'Bill ID', 
    )
    launtype = tables.TemplateColumn('<a href="/laundry/bill={{ record.bill }}/id={{ record.id }}/">{{ record.launtype }}</a>',
                                verbose_name=u'Type',
    )
    change = tables.TemplateColumn('<a href="/laundry/bill={{ record.bill }}/id={{ record.id }}/">Update</a> / <a href="/laundry/{{ record.bill }}/">Add Items</a> / {{record.id}} / '
                                    '<a href="/laundry/bill/{{ record.bill }}/{{record.id}}" onclick="return confirm(\'Are you sure you want to delete this Item?\')">Delete</a>',
                                verbose_name=u'Changes'
    )
    customer = tables.TemplateColumn('{{ record.customer }}',
                                verbose_name=u'Customer Name',
    )
    # change = tables.TemplateColumn('<a href="/schedule/update_schedule/{{ record.id }}">Update</a> / Cancel / Event / '
    #                                '<a href="/schedule/delete_schedule/{{ record.id }}" 
    #                                onclick="return confirm(\'Are you sure you want to delete this Item?\')">Delete</a>',
    #                                verbose_name=u'Change', )
    class Meta:
        model         = LaundryData
        template_name = "django_tables2/bootstrap-responsive.html"
        fields        = ('bill', 'customer', 'launtype', 'quantity', 'price', 'total', 'change',
        )
        # label         = ('رقم الفاتورة','اسم العميل','النوع','الكمية','السعر','الاجمالى','تعديلات',) 

# def render_footer(table):
def render_footer(bound_column, table):
    # s = sum(x['sumtotal'] for x in table.data)
    # s = sum(bound_column.accessor.resolve(row) for row in table.data)
    s = sum(bound_column.accessor.resolve(row) for row in table.data)
    # page = s /  table.paginator.num_pages 

    # row = table.data.
    # if table.paginator.num_pages == 6:
    #     # s = sum(bound_column.accessor.resolve(row) for row in table.data)
    #     return s
    # else:
    #     return ('0000')
    
    # column_total = 0
    # total = record.certificatebills.aggregate(total=Sum(bound_column))
    # column_total += total
    # return total
    return s

class BillsColumn(tables.Column):
    column_total = 0
    def render(self, record):
        bills = record.certificatebills.all()
        total_bill = 0
        for bill in bills:
            total_bill += bill.bill_amount
        # accumulate
        self.column_total += total_bill
        return round(total_bill, 2)

    def render_footer(self, bound_column, table):
        # return round(self.column_total, 2)
    # def render(self, record):
    #     total = record.certificatebills.aggregate(total=Sum("sumtotal"))['total']
    #     self.column_total += total
    #     return total

    # def render_footer(self, bound_column, table):
    #     # return round(self.column_total, 2)
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class LaundryBillTable(tables.Table):
    ''' Here is the solution to make the table items clickable 
    https://stackoverflow.com/questions/44911679/putting-a-click-event-for-a-dialogue-box-with-django-tables2
    '''
    id = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.id }}</a>',
                                verbose_name=u'Bill ID', 
    )
    recieveDate = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.recieveDate }}</a>',
                                verbose_name=u'Recieve Date',
    )
    endDate = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.endDate }}</a>',
                                verbose_name=u'End Date',
    )
    sumtotal = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.sumtotal }}</a>',
                                verbose_name=u'Totals', footer=render_footer
    )
    paid = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.paid }}</a>',
                                verbose_name=u'Paid', footer=render_footer
    )
    remain = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.remain }}</a>',
                                verbose_name=u'Remain', footer=render_footer
    )
    client = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.client }}</a>',
                                verbose_name=u'User',
    )
    # paidDone = tables.TemplateColumn('{{ record.paidDone }}',
    #                              verbose_name=u'Paid Done')
    
    # returns = tables.TemplateColumn('{{ record.returns }}',
    #                              verbose_name=u'Canceled Bill',)
    # name = tables.Column()
    # sumtotal = tables.Column(footer="Total:")
    # population = BillsColumn()
    class Meta:
        model         = LaundryBill
        template_name = "django_tables2/bootstrap4.html"
        fields        = ('id', 'recieveDate', 'endDate', 'sumtotal', 
                        'paid', 'remain', 'client', u'returns', 
        )



class SumLaundryBillTable(tables.Table):
    sumtotal = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.sumtotal }}</a>',
                                verbose_name=u'Totals',
    )
    paid = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.paid }}</a>',
                                verbose_name=u'Paid',
    )
    remain = tables.TemplateColumn('<a href="/laundry/bill/{{ record.id }}/">{{ record.remain}}</a>',
                                verbose_name=u'Remain',
    )
    class Meta:
        model         = LaundryBill
        template_name = "django_tables2/bootstrap4.html"
        fields        = ('sumtotal', 'paid', 'remain',)