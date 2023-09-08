
from django.urls import path
from .views import *

app_name = 'Products_app'

urlpatterns = [
    path('', Home_View.as_view(), name='home'),
    
]