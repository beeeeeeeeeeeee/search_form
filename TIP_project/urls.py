"""TIP_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from search.views import SearchFilterView, models_api, export_csv, MapView, DashbordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashbordView, name='dashboard'),
    path('search/', SearchFilterView, name='search'),
    path('dashboard/', DashbordView, name='dashboard'),
    path('map/',MapView, name='map'),
    path('api/models/', models_api, name='models_api'),
    path('export-csv/', export_csv, name='export_csv')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
