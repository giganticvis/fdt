from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('foi-fod-dashboard/', views.foi_fod_dashboard, name='foi_fod_dashboard'),
    path('ccd-dashboard/', views.ccd_dashboard, name='ccd_dashboard'),
    path('oep-dashboard/', views.oep_dashboard, name='oep_dashboard'),
    path('super-admin-dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('export-flight-data/', views.export_flight_data, name='export_flight_data'),
    path('get-flights/', views.get_flights, name='get_flights'),  # Add this line
    path('view-logs/', views.view_logs, name='view_logs'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.foi_fod_dashboard, name='profile'),
]
