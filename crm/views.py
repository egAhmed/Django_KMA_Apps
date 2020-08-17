import io
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2.paginators import LazyPaginator
from django.urls import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import UserCreationForm
from .forms import ClientsForm, RecordForm, RegisterForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Clients, RecordFirm, Registration
from django.views.generic import TemplateView, ListView
from django_tables2 import SingleTableView
from .tables import ClientsTable
from reportlab.pdfgen import canvas
from django.views.generic.edit import FormMixin
# from crm.reports import MyReport

# Create your views here.
class MainPage(TemplateView):
    template_name = 'crm/mainpage.html'

class ClientsRport(SingleTableView):
    model = Clients
    table_class = ClientsTable
    template_name = "crm/report.html"
    pagination_class = LazyPaginator
    context_object_name = 'queryset'
    def get_query(self):
        queryset = ClientsTable(Clients.objects.all())
        return queryset

# def ClientsRport(request):
#     table = ClientsTable(Clients.objects.all().order_by('-id'))
#     table.paginate(page=request.GET.get("page", 1), per_page=5)
#
#     return render(request, "crm/report.html",
#                            {"table": table,})

# class ClientsListView(FormMixin, SingleTableView):
    # model = Clients
    # table_class = ClientsTable
    # # fields = ('__all__')
    # form_class = ClientsForm
    # template_name = "clients.html"  # "crm/report.html"
    # success_url = "/crm/"

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         object_list = self.model.objects\
    #         .filter(Q(name__icontains=query)| Q(mobile__icontains=query))
    #     else:
    #         object_list = self.model.objects.none()
    #     return object_list
    #
    # def get_success_url(self):
    #     """Return the URL to redirect to after processing a valid form."""
    #     if not self.success_url:
    #         raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
    #     return str(self.success_url)  # success_url may be lazy
    #
    # def get_form_class(self):
    #     """Return the form class to use."""
    #     return self.form_class
    #
    # def get_initial(self):
    #     """Return the initial data to use for forms on this view."""
    #     return self.initial.copy()
    #
    # def get_prefix(self):
    #     """Return the prefix to use for forms."""
    #     return self.prefix
    #
    # def get_form_kwargs(self):
    #     """Return the keyword arguments for instantiating the form."""
    #     kwargs = {
    #         'initial': self.get_initial(),
    #         'prefix': self.get_prefix(),
    #     }
    #     if self.request.method in ('POST', 'PUT'):
    #         kwargs.update({
    #             'data': self.request.POST,
    #             'files': self.request.FILES,
    #         })
    #     return kwargs
    #
    # def get_form(self, form_class=None):
    #     """Return an instance of the form to be used in this view."""
    #     if form_class is None:
    #         form_class = self.get_form_class()
    #     return form_class(**self.get_form_kwargs())
    #
    # def get_context_data(self, **kwargs):
    #     """Insert the form into the context dict."""
    #     if 'form' not in kwargs:
    #         kwargs['form'] = self.get_form()
    #     return super().get_context_data(**kwargs)
    #
    # def form_valid(self,form):
    #     super(ClientsListView,self).form_valid(form)
    #     # Add action to valid form phase
    #     messages.success(self.request, 'Item created successfully!')
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def form_invalid(self,form):
    #     # Add action to invalid form phase
    #     return self.render_to_response(self.get_context_data(form=form))

def HomePage(request):
    query = Clients.objects.all().order_by('-id')
    # qu_rg = RecordFirm.objects.all().order_by('-last_visit')

    paginator = Paginator(query, 5) # Two post per page
    page = request.GET.get('page')
    # search = Clients.objects.filter()
    try:
        cl_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        cl_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        cl_data = paginator.page(paginator.num_pages)

    context = {'query':query,
                'page':page,
                'cl_data':cl_data,
                # 'search':search,
              }
    return render(request, 'list.html', context)
    # return HttpResponse("<h2><p>Hello to our CRM APP.</p></h2>")

def Search(request):
    _search = request.GET.get('q')
    if _search:
        results = Clients.objects.order_by('-id')\
                 .filter(Q(name__icontains=_search)\
                 | Q(phone__icontains=_search)\
                 | Q(mobile__icontains=_search))
        # results = Clients.objects.filter(name__search=query)
    else:
        results = Clients.objects.all().order_by('-id')


    paginator = Paginator(results, 5) # One result per page
    page = request.GET.get('page')
    try:
        search_result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        search_result = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        search_result = paginator.page(paginator.num_pages)

    context={ 'search_res':search_result,
              'page':page,
              'results':results,
            }

    return render(request, 'tables.html', context)

# def LoginForm(request):
#     return render(request, 'index.html')
#

def RegisterData(request):
    # query = Clients.objects.order_by('-id')
    regdata = RecordFirm.objects.all().order_by('-id')
    paginator = Paginator(regdata, 3) # one post per page
    page = request.GET.get('page')
    # search = Clients.objects.filter()
    try:
        reg_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        reg_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        reg_data = paginator.page(paginator.num_pages)
    context = {
        'data':regdata,
        'reg_data':reg_data,
        'page':page,
    }
    return render(request, 'list.html', context)
    # return HttpResponse("<h2><p>Hello to our CRM APP.</p></h2>")


def SaveDone(request):
    message = 'Saving Done Successfully'
    # images  = '/crm/img/crm1.jpeg'
    context = {
        'message':message, #'images':images,
    }
    return render(request,'savedone.html', context)


def EditFirm(request):
    # client = Clients.objects.order_by('-id')
    recordfirm = RecordFirm.objects.order_by('-id')
    context= {
        # 'client':client,
        'recordfirm':recordfirm,
    }

    return render(request, 'tables.html', context)


def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/done')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def Firm(request): # Saving registration
    # rec = RecordFirm.objects.order_by('-id')
    if request.method == "POST":
        form = RecordForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
            # return redirect('/record/edit/')
            return HttpResponseRedirect(instance.get_url())
    else:
        form = RecordForm()


    context = {
        'form':form,
        'btn':'Save',
    }

    return render(request,'forms.html', context) #forms.html


def Firm_Update(request, id):
    # client = Clients.objects.get(id=id)
    instance = RecordFirm.objects.get(id=id)
    # recField = RecordFirm.objects.order_by('-id')
    form = RecordForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save()
        instance.save()
        return HttpResponseRedirect(instance.get_url())

    context = {
        'instance':instance,
        # 'recField':recField,
        'form':form,
        'btn':'Update',
    }

    return render(request,'forms.html', context) #forms.html

# To assign client name when client id changed
# def GoToId(request):
#     # client = Clients.objects.last()
#     # client = Clients.objects.latest("id")
#     client = RecordFirm.objects.latest('client_id') #
#     # client = RecordFirm.objects.get(id=56)
#     #cl_id = client.id
#
#     form = RecordForm(request.GET or None, instance=client)
#     if form.is_valid():
#         instance = form.save()
#         instance.save()
#         # return HttpResponseRedirect(instance.get_url())
#
#     context = {
#         'client':client,
#         # 'cl_id':cl_id,
#         'form':form,
#         'equal':'=',
#     }
#     return render(request, 'forms.html', context)


def EditClients(request):
    client = Clients.objects.order_by('-id')
    # recordfirm = RecordFirm.objects.all()
    context= {
        'client':client,
        # 'rec':recordfirm,
    }
    return render(request, 'tables.html', context)


def ClientID(request, id): # update form , (request, id, name, phone, address)
    # instance = Clients.objects.get(id=id, name=name, phone=phone, address=address)
    instance = Clients.objects.get(id=id)
    form = ClientsForm(request.POST or None, request.FILES or None, instance=instance)
    # form = ClientsForm(request.POST or None, name=name, phone=phone)
    # client = get_object_or_404(Clients, id=id)
    # form = ClientsForm(request.GET)
    # client = Clients.objects.get(id=id)
    # recordfirm = RecordFirm.objects.all()
    # if request.method != 'POST':
    if form.is_valid():
        form.save()
        # instance = form.save()
        # instance.save()
        return HttpResponseRedirect(instance.goto_home())
    # else:
    #     form = ClientsForm()

    context= {
        'form': form,
        'instance':instance,
        'btn':'Update',
        'comp':'Update Company Data',
        'New':'Add Company',
    }
    return render(request, 'clients.html', context)


def ClientName(request):
    # client = get_object_or_404(Clients, id=id)
    # table = ClientsTable(Clients.objects.all())
    if request.method == 'POST':
        form = ClientsForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance = Clients(photo=request.FILES['photo'])
            instance.save()
            # form.save()
            # return HttpResponseRedirect(instance.get_absolute_url())

            return HttpResponseRedirect('/crm/')
            # return HttpResponseRedirect(reverse('crm:clients_id', args=(id,)))
    else:
        form = ClientsForm()

    context = {
            'form': form,
            'btn': 'Save',
            'comp':'Save Company Data',
            'New':'Home Page',
            # 'table':table,
    }
    return render(request, 'clients.html', context) #clients.html


# def user_register(request):
#     # if this is a POST request we need to process the form data
#     template = 'register.html'

#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = RegisterForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             if User.objects.filter(username=form.cleaned_data['username']).exists():
#                 return render(request, template, {
#                     'form': form,
#                     'error_message': 'Username already exists.'
#                 })
#             elif User.objects.filter(email=form.cleaned_data['email']).exists():
#                 return render(request, template, {
#                     'form': form,
#                     'error_message': 'Email already exists.'
#                 })
#             elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
#                 return render(request, template, {
#                     'form': form,
#                     'error_message': 'Passwords do not match.'
#                 })
#             else:
#                 # Create the user:
#                 user = User.objects.create_user(
#                                 form.cleaned_data['username'],
#                                 form.cleaned_data['email'],
#                                 form.cleaned_data['password']
#                 )
#                 user.first_name = form.cleaned_data['first_name']
#                 user.last_name = form.cleaned_data['last_name']
#                 user.phone_number = form.cleaned_data['phone_number']
#                 user.save()

#                 # Login the user
#                 login(request, user)

#                 # redirect to accounts page:
#                 return HttpResponseRedirect('signup')

#    # No post data availabe, let's just show the page.
#     else:
#         form = RegisterForm()

#     return render(request, template, {'form': form})
