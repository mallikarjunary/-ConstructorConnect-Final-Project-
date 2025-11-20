from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from user.models import *
from contractor.models import *

# Create your views here.
def adminusersview(request):
    data = Usermodel.objects.all()
    return render(request, 'admins/adminhome.html', {'data': data})

def adminactivateuser(request):
    uid = request.GET.get('uid')
    user = get_object_or_404(Usermodel, id=uid)
    
    if user.is_active:
        messages.info(request, 'User is already activated.')
    else:
        user.is_active = True
        user.save()
        messages.success(request, 'User activated successfully.')

    return redirect('adminusersview')

def admincontractorview(request):
    data = Contractormodel.objects.all()
    return render(request, 'admins/admincontractorview.html', {'data': data})

def adminactivatecontractor(request):
    uid = request.GET.get('uid')
    user = get_object_or_404(Contractormodel, id=uid)
    
    if user.is_active:
        messages.info(request, 'User is already activated.')
    else:
        user.is_active = True
        user.save()
        messages.success(request, 'User activated successfully.')

    return redirect('admincontractorview')

def adminusercontractview(request):
    data = HouseBiddingmodel.objects.all()
    return render(request, 'admins/adminusercontractview.html', {'data': data})

def admincontractorbidsview(request):
    # Query all active house biddings and their related contractor bids
    contractor_bids = []
    
    house_biddings = HouseBiddingmodel.objects.all()
    for house in house_biddings:
        bids = ContractorBidmodel.objects.filter(property_id=house.id)
        for bid in bids:
            contractor_bids.append({
                'house_bidding': house,
                'bid': bid
            })

    # Pass the data to the template
    context = {
        'contractor_bids': contractor_bids
    }
    return render(request, 'admins/admincontractorbidsview.html', context)