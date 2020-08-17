from django import forms
from django.core import validators
from crm.models import Clients
from .models import LaundryBill, LaundryData, Customers

class LaundryBillForm(forms.ModelForm):
    # def twenty_years():
    #     year = None
    #     for i in range(1,25):
    #         year = 2000
    #         year = year + i
    #     return year

    # YEAR_CHOICES = ['1980', '1981', '1982','2000','2019','2020','2021','2022','2023']
    true_or_false = [
                    ('False', 'false'),
                    ('True', 'true'),
    ]

    recieveDate = forms.DateField(
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'datepicker1',
                'name': 'recievedate',
                'placeholder':'2020-05-01'
            }
        )
    )
    # recieveDate = forms.DateField(label='Recieve Date',
    #     widget=forms.SelectDateWidget(empty_label=( "Choose Year", 
    #                                                 "Choose Month",
    #                                                 "Choose Day"),years=twenty_years(),
    #         attrs={
    #             'class':'col-8 mr-auto',
    #             'id':'recievedate',
    #             'name':'recievedate',
    #         }
    #     )
    # )
    endDate = forms.DateField(label='Delivered Date',
        widget=forms.DateInput(
            attrs={
                'class':'form-control',
                'id':'enddate',
                'name':'enddate', 
                'placeholder':'2020-05-01'
            }
        )
    )
    sumtotal = forms.FloatField(label='Total',
        widget=forms.NumberInput(
            attrs={ 
                'class':'form-control',
                'id':'sumtotal',
                'name':'sumtotal'
            }
        )
    )
    paid = forms.FloatField(label='Paid',
        widget=forms.NumberInput(
            attrs={ 
                'class':'form-control',
                'id':'paid',
                'name':'paid'
            }
        )
    )
    remain = forms.FloatField(label='Remain',
        widget=forms.NumberInput(
            attrs={ 
                'class':'form-control',
                'id':'remain',
                'name':'remain'
            }
        )
    )
    client = forms.ModelChoiceField(queryset=Clients.objects.all(), label='User',
        widget=forms.Select(
            attrs={ 
                'class':'form-control',
                'id':'client',
                'name':'client'
            }
        )
    )
    # paidDone = forms.ChoiceField(label='Paid Done', choices=true_or_false, required=False,
    paidDone = forms.ChoiceField(label='Paid Done', choices=true_or_false, required=False,
        widget=forms.Select(
            attrs={ 
                'class':'form-control',
                'id':'paidDone',
                'name':'paidDone',
                # 'value':''
            }
        )
    )
    returns = forms.BooleanField(label='Canceled',required=False,
        widget=forms.CheckboxInput(
            attrs={ 
                'class':'checkbox m-15',
                'type':'checkbox',
                'id':'returns',
                'name':'returns',
                # 'checked':'False',
            }
        )
    )
    
    class Meta:
        model = LaundryBill
        fields = ('recieveDate', 'endDate', 'sumtotal', 
                  'paid', 'remain', 'client','paidDone','returns',
        )

        # FAVORITE_COLORS_CHOICES = [
        #     ('blue', 'Blue'),
        #     ('green', 'Green'),
        #     ('black', 'Black'),
        # ]
        
        # favorite_colors = forms.MultipleChoiceField(
        #         required=False,
        #         widget=forms.CheckboxSelectMultiple,
        #         choices=FAVORITE_COLORS_CHOICES,
        #     )
        
class LaundryDataForm(forms.ModelForm):
    # def __init__(self,*args, **kwargs):
    #     self.bill = kwargs.get('id')
    #     super(LaundryDataForm, self).__init__(*args, **kwargs)
    #     self.fields['bill'].queryset = LaundryBill.objects.filter(id=self.bill)
    
    def get_queryset(*args, **kwargs):
        # bill = kwargs.get('id')
        # queryset = LaundryBill.objects.filter(id=kwargs.get('id')).last()
        queryset = LaundryBill.objects.all()#filter(id=kwargs.get('id')).last()
        return queryset

    # def clean(self):
    #     # cleaned_data = super().clean()
    #     total = self.cleaned_data.get('total')
    #     customer = self.cleaned_data.get('customer')
    #     bill = self.cleaned_data.get('bill')

    #     if total == 0:
    #         raise forms.ValidationError("Total must be a number not a zero")
    #         return total

    launtype  = forms.CharField(label='Type', required=True, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'name':'launtype',
                'id':'launtype'
            }
        )
    )
    quantity  = forms.IntegerField(label='Quantity', required=True, 
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'name':'quantity',
                'id':'quantity'
            }
        )
    )
    price     = forms.FloatField(label='Price', required=True, 
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'name':'price',
                'id':'price'
            }
        )
    )
    total     = forms.FloatField(label='Totals',  
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'name':'total',
                'id':'total',
                # 'value':'00.00'
                # 'disabled':'True'
            }
        )
    )
    customer  = forms.ModelChoiceField(queryset=Customers.objects.all(), label='Customer No',
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'name':'customer',
            }
        )
    )
    bill = forms.ModelChoiceField(queryset=get_queryset(), label='Bill ID',
        widget=forms.Select(
            attrs={ 
                'class':'form-control',
                'name':'bill',
            }
        )
    )

    class Meta:
        model = LaundryData
        fields = ('__all__') 
        # label =('النوع','الكمية','السعر','رقم العميل','رقم الفاتورة')
        # bill = forms.CharField(
        # widget=forms.TextInput(
        #         attrs={ 'class':'form-control',
        #                 'name':'bill'
        #         }
        # )
        # )