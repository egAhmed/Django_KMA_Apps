from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import RecordFirm, Clients


class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(
                                attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
                                attrs={'class': 'form-control'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}), required=False)
    phone_number = forms.CharField(widget=forms.NumberInput(
                                attrs={'class':'form-control'}), required=False)


    # vitor site
    # email = forms.CharField(widget=forms.TextInput(
    #     attrs={'placeholder': 'Email'}))

    # password = forms.CharField(widget=forms.PasswordInput())

    # address_1 = forms.CharField(
    #             label='Address',widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    # )
    # address_2 = forms.CharField(
    #             widget=forms.TextInput(
    #             attrs={'placeholder': 'Apartment, studio, or floor'})
    # )
    # city = forms.CharField()
    # state = forms.ChoiceField(choices=STATES)
    # zip_code = forms.CharField(label='Zip')
    # check_me_out = forms.BooleanField(required=False)

class RecordForm(forms.ModelForm):
    #
    type = forms.ChoiceField(choices=RecordFirm.Currency,
                             widget=forms.RadioSelect,
                             label='Type of Payment',
                             required=False)
    # widget=forms.RadioSelect

    # firm_name = forms.CharField(widget=forms.TextInput(), label='Company Name', required=True)
    # manager = forms.CharField(widget=forms.TextInput(), required=True)
    # repres_name = forms.CharField(widget=forms.TextInput(), required=True)

    last_visit = forms.DateField(widget=AdminDateWidget, required=True)
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    # last_visit = forms.DateTimeField()

    # (
    #                         input_formats=['%d/%m/%Y %H:%M'],
    #                         widget=forms.DateInput(attrs={
    #                         'class': 'form-control datetimepicker-input',
    #                         'data-target': '#datepicker',
    #                         'type': 'date'})
    # )

    class Meta:
        model = RecordFirm
        # 'client',
        # fields = ('__all__')

        fields = ('client_id', 'Company Name', 'type', 'manager',
                  'repres_name','last_visit','notes',
                  'tax_no','part_no','purchase_no')

        widgets = {'last_visit': forms.DateInput(
                    attrs={'class': 'datepicker'}),
                    # 'firm_name':forms.TextInput(
                    #     attrs={'label':'Company Name'}
                    # )
                #    'type': forms.BooleanField(),
                #    'part_no': forms.BooleanField(),
                #    'purchase_no': forms.BooleanField(),
                    # 'notes': 'required=False',
                   }

    # class Meta:
    #     model = RecordFirm
    #     fields = ('Company Name', 'manager',
    #               'repres_name','notes','type',)


    # class RecordForm(forms.ModelForm):
    #     type = forms.ChoiceField(
    #                 choices=RecordFirm.PAPERS, widget=forms.RadioSelect)
    # last = forms.DateTimeField(
    #                 input_formats=['%d/%m/%Y %H:%M'],
    #                 widget=forms.DateTimeInput(attrs={
    #                 'class': 'form-control datetimepicker-input',
    #                 'data-target': '#datetimepicker'})
    # )
    # firm_name = forms.CharField()
    # manager = forms.CharField()
    # repres_name = forms.CharField()
    # last_visit = forms.DateTimeField(
    #                         input_formats=['%d/%m/%Y %H:%M'],
    #                         widget=forms.DateTimeInput(attrs={
    #                         'class': 'form-control datetimepicker-input',
    #                         'data-target': '#datetimepicker'})
    # )
    # notes = forms.Textarea()
    # # ('firm_name', 'manager', 'repres_name', 'last_visit', 'notes', )

class ClientsForm(forms.ModelForm):
    
    # def clean(self):
    #     request = self.request
    #     data = self.cleaned_data
    #     name = data.get('name')
    #     if user.is_authenticated:
    #         raise forms.ValidationError('You are authenticated')
    #     else:
    #         raise forms.ValidationError('You must login')

    #     return data


    class Meta:
        model  = Clients
        fields = ('__all__')
        # label  = ('Client Name', 'Tel No', 'Cell No') 
    
    def clean(self):
        # request = self.request
        data = self.cleaned_data
        name = data.get('name')
        if name == 'm':
            raise forms.ValidationError('Enter a valid name')

        # if username.is_authenticated:
        #     raise forms.ValidationError('You are authenticated')
        # else:
        #     raise forms.ValidationError('You must login')

        return data
