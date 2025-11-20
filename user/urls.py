from django.contrib import admin
from django.urls import path
from user.views import *

urlpatterns = [
     path('userregistraction', userregistraction, name='userregistraction'),
     path('user_verify_otp/', user_verify_otp, name='user_verify_otp'),
     path('userhome', userhome, name='userhome'),
     path('userpredictpage', userpredictpage, name='userpredictpage'),
     path('predict_price/', predict_price, name='predict_price'),
     path('update_profile', update_profile, name='update_profile'),
     path('userhousebiddingpage/', userhousebiddingpage, name='userhousebiddingpage'),
     path('userhousebiddingpageaction/', userhousebiddingpageaction, name='userhousebiddingpageaction'),
     path('housebiddingdeactivate/', housebiddingdeactivate, name='housebiddingdeactivate'),
     path('contractorbids/', contractorbids, name='contractorbids'),
     path('handle_bids/', handle_bids, name='handle_bids'),
     path('usercheckpropertyupdates/', usercheckpropertyupdates, name='usercheckpropertyupdates'),
     path('check_images/<int:update_id>/', check_images, name='check_images'),
]