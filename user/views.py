from django.shortcuts import render, redirect, get_object_or_404
from user.models import *
from contractor.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

import pickle
import pandas as pd
import yagmail
import random


# Create your views here.
def userregistraction(request):
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

                return render(request, 'user/otppage.html')
            
        except Exception as e:
            print(f'Error sending email: {e}')
            message = 'Failed to send OTP. Please try again later.'
            return render(request, 'loginpage.html', {'message': message})
    else:
        message = 'Registration un-successfull'
        return render(request, 'loginpage.html', {'message': message})
    
def user_verify_otp(request):
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
            
            form1 = Usermodel(username=username, password=password, email=email, phone=phone, city=city, state=state, country=country)
            form1.save()
            
            message = 'Registration successful'
            return render(request, 'loginpage.html', {'message': message})
        else:
            message = 'Invalid OTP. Please try again.'
            return render(request, 'otppage.html', {'message': message})
    else:
        return redirect('loginpage')
        
def userhome(request):
    user_id = request.session.get('user_id')
    user = Usermodel.objects.get(id=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'user/userhome.html', context)

def userpredictpage(request):
    return render(request, 'user/userpredictpage.html')

def update_profile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = Usermodel.objects.get(id=user_id) 

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
        return redirect('userhome')  
    else:
        return redirect('userhome')
    

def predict_price(request):
    if request.method == 'POST':
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        sqft_living = request.POST.get('sqft_living')
        sqft_lot = request.POST.get('sqft_lot')
        floors = request.POST.get('floors')
        waterfront = request.POST.get('waterfront')
        sqft_above = request.POST.get('sqft_above')
        sqft_basement = request.POST.get('sqft_basement')
        sqft_living15 = request.POST.get('sqft_living15')
        sqft_lot15 = request.POST.get('sqft_lot15')
        print(bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, sqft_above,sqft_basement, sqft_living15, sqft_lot15)

        def predict_price_with_loaded_model(features):
            feature_names = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'sqft_above', 'sqft_basement', 'sqft_living15', 'sqft_lot15']
            input_data = pd.DataFrame([features], columns=feature_names)
            with open(r'media\model\house_price_model.pkl', 'rb') as file:
                loaded_model = pickle.load(file)
            predicted_price = loaded_model.predict(input_data)
            return predicted_price[0]
        
        example_features = {
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft_living': sqft_living,
            'sqft_lot': sqft_lot,
            'floors': floors,
            'waterfront': waterfront,
            'sqft_above': sqft_above,
            'sqft_basement': sqft_basement,
            'sqft_living15': sqft_living15,
            'sqft_lot15': sqft_lot15
        }
        
        predicted_price = predict_price_with_loaded_model(example_features)
        print(predicted_price)
        return render(request, 'user/userpredictpage.html', {'message': predicted_price})
    else:
        messages.error(request, 'Model crashed!')
        return render(request, 'user/userpredictpage.html')
    
def userhousebiddingpage(request):
    user_id = request.session.get('user_id')
    user = Usermodel.objects.get(id=user_id)
    Bids = HouseBiddingmodel.objects.filter(user=user) 
    return render(request, 'user/userhousebiddingpage.html', {'data': Bids})

def userhousebiddingpageaction(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = Usermodel.objects.get(id=user_id)

        Title = request.POST.get('title')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        sqft_total = request.POST.get('sqft_total')
        floors = request.POST.get('floors')
        house_type = request.POST.get('house_type')
        state = request.POST.get('state')
        city = request.POST.get('city')
        country = request.POST.get('country')
        Budget = request.POST.get('budget')
        print(user, bedrooms, bathrooms, sqft_total, floors, house_type, state,city, country, Budget, Title)

         # Email details
        user_email = 'chandukommineni22@gmail.com'
        app_password = 'xqyktinvcvfjuuyw'
        subject = 'New Contract has been Uploaded'
        content = f'''
            <p>Dear Contractor,</p>
            <p>We have an exciting contract for you.</p>
            <p>Bedrooms: {bedrooms}</p>
            <p>Bathrooms: {bathrooms}</p>
            <p>Floors: {floors}</p>
            <p>Look into your dashboard for more bidding details.</p>
            <p>Regards,</p>
            <p>Team Upconstruction</p>
        '''

        # Send emails to contractors in the specified city and state
        contractors = Contractormodel.objects.filter(city=city, state=state)
        contractor_emails = [contractor.email for contractor in contractors]
        print(contractor_emails)

        with yagmail.SMTP(user_email, app_password) as yag:
            for email in contractor_emails:
                yag.send(email, subject, content)
                print(f'Sent email to contractor: {email}')

        HouseBiddingmodel.objects.create(
            user=user,
            Title=Title,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            sqft_total=sqft_total,
            floors=floors,
            house_type=house_type,
            state=state,
            city=city,
            country=country,
            Budget = Budget
        )
        Bids = HouseBiddingmodel.objects.filter(user=user)
        
        return render(request, 'user/userhousebiddingpage.html', {'data': Bids})
    else:
        return render(request, 'user/userhousebiddingpage.html')
    
def housebiddingdeactivate(request):
    uid = request.GET.get('uid')
    user = get_object_or_404(HouseBiddingmodel, id=uid)
    user.is_active = False
    user.save()
    messages.success(request, 'Bid Closed')
    return redirect('userhousebiddingpage')

def contractorbids(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  

    try:
        user = Usermodel.objects.get(id=user_id)
    except Usermodel.DoesNotExist:
        return redirect('error_page')

    house_biddings = HouseBiddingmodel.objects.filter(user=user.username)  
    contractor_bids = []

    if house_biddings.exists():
        bids = ContractorBidmodel.objects.filter(property_id__in=house_biddings.values_list('id', flat=True))
        for bid in bids:
            house_bidding = house_biddings.get(id=bid.property_id)
            existing_status = UserBidAcceptedRejectedmodel.objects.filter(
                user=user.username,
                property_id=bid.property_id,
                contractor_bid_id=bid.id
            ).first()

            contractor_bids.append({
                'bid': bid,
                'house_bidding': house_bidding,
                'existing_status': existing_status
            })

    return render(request, 'user/contractorbids.html', {
        'contractor_bids': contractor_bids
    })

def handle_bids(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = Usermodel.objects.get(id=user_id)

        for key, value in request.POST.items():
            if key.startswith('status_') and value:
                bid_id = key.split('_')[1]
                status = value
                property_id = request.POST.get(f'property_id_{bid_id}')
                
                contractor_bid = ContractorBidmodel.objects.get(id=bid_id)
                house_bidding = HouseBiddingmodel.objects.get(id=property_id)
                print(user.username, house_bidding.id, contractor_bid.id, status)
                UserBidAcceptedRejectedmodel.objects.create(
                    user=user.username,
                    property_id=house_bidding.id,
                    contractor_bid_id=contractor_bid.id,
                    status=status
                )

        return redirect('contractorbids') 

    return redirect('contractorbids')

def usercheckpropertyupdates(request):
    user_id = request.session.get('user_id')
    updates = ContractorWeeklyUpdateActionModel.objects.filter(user_id=user_id)
    context = {
        'updates': updates
    }
    return render(request, 'user/usercheckpropertyupdates.html', context)

def check_images(request, update_id):
    update = get_object_or_404(ContractorWeeklyUpdateActionModel, id=update_id)
    images = update.images.all()
    property_id = update.property_id

    context = {
        'images': images,
        'property_id': property_id,
    }

    return render(request, 'user/images.html', context)