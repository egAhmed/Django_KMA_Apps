"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
# import forms_builder.forms.urls
from django.conf import settings
from django.conf.urls.static import static
from jobs import views  # jobs.views
from accounts import views  # accounts.views
from crm.views import MainPage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='mainpage'),
    # path('forms/', include(forms_builder.forms.urls)),
    path('crm/', include('crm.urls', namespace='KMA_CRM')),
    path('blog/', include('blog.urls', namespace='blog')),
    # path('signup/', include('accounts.urls', namespace='accounts')),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('jobs/', include('jobs.urls', namespace='amr_jobs')),
    path('laundry/', include('laundry.urls', namespace='laundry')),
    path('amrblog/', include('amrblog.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #\
  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
