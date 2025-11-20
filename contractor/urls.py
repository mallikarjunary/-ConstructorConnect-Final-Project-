from django.contrib import admin
from django.urls import path
from contractor.views import *

urlpatterns = [
    path('contractorregistraction/', contractorregistraction, name='contractorregistraction'),
    path('contractor_verify_otp/', contractor_verify_otp, name='contractor_verify_otp'),
    path('contractorhome', contractorhome, name='contractorhome'),
    path('update_con_profile', update_con_profile, name='update_con_profile'),
    path('housingbids/', housingbids, name='housingbids'),
    path('contractorbiddingaction/', contractorbiddingaction, name='contractorbiddingaction'),
    path('contractorcontracts/', contractorcontracts, name='contractorcontracts'),
    path('update_bid/<int:bid_id>/', contractor_update_bid, name='update_bid'),
    path('contractorweeklyupdateaction/', contractorweeklyupdateaction, name='contractorweeklyupdateaction'),
    path('contractor_check_images/<int:update_id>/', contractor_check_images, name='contractor_check_images'),
]