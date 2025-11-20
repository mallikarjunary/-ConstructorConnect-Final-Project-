from django.contrib import admin
from django.urls import path
from admins.views import *

urlpatterns = [
    path('adminusersview/', adminusersview, name='adminusersview'),
    path('adminactivateuser/', adminactivateuser, name='adminactivateuser'),
    path('admincontractorview/', admincontractorview, name='admincontractorview'),
    path('adminactivatecontractor/', adminactivatecontractor, name='adminactivatecontractor'),
    path('adminusercontractview/', adminusercontractview, name='adminusercontractview'),
    path('admincontractorbidsview/', admincontractorbidsview, name='admincontractorbidsview'),
]