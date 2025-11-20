from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from contractor.models import *
from user.models import *
from django.contrib import messages
import yagmail
import random

# Create your views here.
def contractorregistraction(request):
    if request.method=='POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city') 
        state = request.POST.get('state')
        country = request.POST.get('country')
        print(username, password, phone, email, city, state, country)

        otp = str(random.randint(1000, 9999))

        user1 = 'chandukommineni22@gmail.com' 
        app_password = 'xqyktinvcvfjuuyw'

        subject = 'OTP for Registration'
        content = f'''
        <p>Dear User,</p>
        <p>Your OTP for registration is: {otp}</p>
        <p>Please use this OTP to complete your registration.</p>
        <p>Regards,</p>
        <p>Team Upconstruction</p>
        '''

        try:
            with yagmail.SMTP(user1, app_password) as yag:
                yag.send(email, subject, content)
                print('Sent email successfully')
   
                request.session['otp'] = otp
                request.session['username'] = username
                request.session['password'] = password
                request.session['email'] = email
                request.session['phone'] = phone
                request.session['city'] = city
                request.session['state'] = state
                request.session['country'] = country

                return render(request, 'contractor/otppage.html')
            
        except Exception as e:
            print(f'Error sending email: {e}')
            message = 'Failed to send OTP. Please try again later.'
            return render(request, 'loginpage.html', {'message': message})
    else:
        message = 'Registration un-successfull'
        return render(request, 'loginpage.html', {'message': message})
    
def contractor_verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_sent = request.session.get('otp')
        
        if otp_entered == otp_sent:
            username = request.session.get('username')
            password = request.session.get('password')
            email = request.session.get('email')
            phone = request.session.get('phone')
            city = request.session.get('city')
            state = request.session.get('state')
            country = request.session.get('country')

            form1 = Contractormodel(username=username, password=password, email=email, phone=phone, city=city, state=state, country=country)
            form1.save()
            
            message = 'Registration successful'
            return render(request, 'loginpage.html', {'message': message})
        else:
            message = 'Invalid OTP. Please try again.'
            return render(request, 'otppage.html', {'message': message})
    else:
        return redirect('loginpage')

def contractorhome(request):
    user_id = request.session.get('user_id')
    user = Contractormodel.objects.get(id=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'contractor/contractorhome.html', context)

def update_con_profile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = Contractormodel.objects.get(id=user_id) 

        if request.POST.get('email'):
            user.email = request.POST.get('email')
        if request.POST.get('phone'):
            user.phone = request.POST.get('phone')
        if request.POST.get('city'):
            user.city = request.POST.get('city')
        if request.POST.get('state'):
            user.state = request.POST.get('state')
        if request.POST.get('country'):
            user.country = request.POST.get('country')

        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('contractorhome')  
    else:
        return redirect('contractorhome')

def housingbids(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    try:
        user = Contractormodel.objects.get(id=user_id)
    except Contractormodel.DoesNotExist:
        return redirect('error_page')

    bids = ContractorBidmodel.objects.filter(contractor=user)
    dataa = []

    for bid in bids:
        try:
            property = HouseBiddingmodel.objects.get(id=bid.property_id)
            dataa.append({
                'id': property.id,
                'bedrooms': property.bedrooms,
                'bathrooms': property.bathrooms,
                'sqft_total': property.sqft_total,
                'floors': property.floors,
                'house_type': property.house_type,
                'city': property.city,
                'state': property.state,
                'Budget': property.Budget,
                'bid_amount': bid.bid_amount,
            })
        except HouseBiddingmodel.DoesNotExist:
            pass 

    data = HouseBiddingmodel.objects.filter(city=user.city, state=user.state, is_active=True)
    
    return render(request, 'contractor/contractorbids.html', {'data': data, 'dataa': dataa})

def contractorbiddingaction(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        contractorbid = request.POST.get('contractorbid')
        print(uid, contractorbid)

        user_id = request.session.get('user_id')
        user = Contractormodel.objects.get(id=user_id)

        data = HouseBiddingmodel.objects.get(id = uid)
        d1 = Usermodel.objects.get(username = data.user)
        d2 = d1.email
        print(d2)

        user1 = 'chandukommineni22@gmail.com'
        app_password = 'xqyktinvcvfjuuyw' 
        to = d2
        subject = 'You had got an New Bid'
        content = f'''
        <p>Dear User,</p>
        <p>We have an exciting contract for you.</p>
        <p>Bid Amount:{contractorbid}</p>
        <p>Regards,</p>
        <p>Team Upconstruction</p>
        </table>
        '''
        with yagmail.SMTP(user1, app_password) as yag:
            yag.send(to, subject, content)
            print('Sent email successfully')

        bid = ContractorBidmodel(
            contractor=user,
            property_id=uid,
            bid_amount=contractorbid
        )
        bid.save()

    return redirect('housingbids')

# def contractorcontracts(request):
#     user_id = request.session.get('user_id') 
#     try:
#         contractor = Contractormodel.objects.get(id=user_id)
#         contractor_bids = ContractorBidmodel.objects.filter(contractor=contractor)
#         bid_ids = contractor_bids.values_list('id', flat=True)
#         bids = UserBidAcceptedRejectedmodel.objects.filter(contractor_bid_id__in=bid_ids)
        
#         context = {
#             'contractor': contractor,
#             'bids': bids,
#         }
#         return render(request, 'contractor/contractorcontracts.html', context)
#     except Contractormodel.DoesNotExist:
#         return render(request, 'contractor/contractorcontracts.html', {'error': 'Contractor not found'})

def contractorcontracts(request):
    user_id = request.session.get('user_id')
    try:
        contractor = Contractormodel.objects.get(id=user_id)
        contractor_bids = ContractorBidmodel.objects.filter(contractor=contractor.username)
        bid_ids = contractor_bids.values_list('id', flat=True)
        bids = UserBidAcceptedRejectedmodel.objects.filter(contractor_bid_id__in=bid_ids)

        bids_with_titles = []
        for bid in bids:
            try:
                property_title = HouseBiddingmodel.objects.get(id=bid.property_id).Title
            except HouseBiddingmodel.DoesNotExist:
                property_title = 'N/A'
            bids_with_titles.append({
                'id': bid.id,
                'property_title': property_title,
                'user': bid.user,
                'status': bid.status,
            })

        context = {
            'contractor': contractor,
            'bids': bids_with_titles,
        }
        return render(request, 'contractor/contractorcontracts.html', context)
    except Contractormodel.DoesNotExist:
        return render(request, 'contractor/contractorcontracts.html', {'error': 'Contractor not found'})


def contractor_update_bid(request, bid_id):
    bid = get_object_or_404(UserBidAcceptedRejectedmodel, id=bid_id)
    user_details = get_object_or_404(Usermodel, username=bid.user)
    property_details = get_object_or_404(HouseBiddingmodel, id=bid.property_id)

    weekly_updates = ContractorWeeklyUpdateActionModel.objects.filter(
        user_id=user_details.id, 
        property_id=property_details.id
    )
    
    context = {
        'bid': bid,
        'user_details': user_details,
        'property_details': property_details,
        'weekly_updates': weekly_updates,
    }
    return render(request, 'contractor/contractorgiveupdate.html', context)


def contractorweeklyupdateaction(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        title = request.POST.get('title')
        description = request.POST.get('description')
        cost_utilized = request.POST.get('cost_utilized')
        user_id = request.POST.get('user_id')
        property_id = request.POST.get('property_id')
        contractor_id = request.session.get('user_id')
        update_action = ContractorWeeklyUpdateActionModel(
            from_date=from_date,
            to_date=to_date,
            title=title,
            description=description,
            cost_utilized=cost_utilized,
            user_id=user_id,
            property_id=property_id,
            contractor_id=contractor_id
        )
        update_action.save()
        if request.FILES.getlist('images'):
            images = request.FILES.getlist('images')
            fs = FileSystemStorage()
            for image_file in images:
                filename = fs.save(image_file.name, image_file)
                uploaded_file_url = fs.url(filename)
                UpdateActionImage(update_action=update_action, image=uploaded_file_url).save()

        return redirect('contractorcontracts')

    return render(request, 'contractorcontracts.html')

def contractor_check_images(request, update_id):
    update = get_object_or_404(ContractorWeeklyUpdateActionModel, id=update_id)
    images = update.images.all()
    property_id = update.property_id

    context = {
        'images': images,
        'property_id': property_id,
    }

    return render(request, 'contractor/images.html', context)