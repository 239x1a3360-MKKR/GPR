"""
URL configuration for virtuallab project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lab/', include('lab.urls')),
    path('api/', include('lab.urls')),
    path('', RedirectView.as_view(url='/lab/', permanent=False)),
]

# Admin branding
admin.site.site_header = "GPREC Administration"
admin.site.site_title = "GPREC Admin Portal"
admin.site.index_title = "Welcome to GPREC Code Lab Admin"

