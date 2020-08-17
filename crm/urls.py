from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from crm import views
from crm.views import *  # HomePage,Search,SaveDone

app_name = "crm"
urlpatterns = [
    path('', views.HomePage, name='home'),
    path('results/', views.Search, name='search'),
    path('registerdata/', views.RegisterData, name='regdata'),
    path('done/', views.SaveDone, name='done'),
    # path('reports/', views.ClientsRport, name='clientreport'),
    path('reports/', ClientsRport.as_view(), name='clientreport'),
    # path('clients/', ClientsListView.as_view(), name='clients'),
    path('clients/edit/', views.EditClients, name='clients_edit'),
    # path('clients/edit/<int:id>/', views.ClientID, name='clients_update'),
    path('clients/edit/<int:id>/',
                views.ClientID, name='clients_update'),
    path('clients/', views.ClientName, name='clients'),
    # path('login/', views.LoginForm, name='login'),
    # path('signup/', views.signup, name='signup'),
    # path('register/', views.user_register, name='user_register'),
    path('record/', views.Firm, name='record_firm'),
    path('record/edit/', views.EditFirm, name='edit'),
    path('record/<int:id>/', views.Firm_Update, name='firm_update'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
