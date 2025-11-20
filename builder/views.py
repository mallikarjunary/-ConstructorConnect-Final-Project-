from django.shortcuts import render
from django.contrib import messages
from user.models import *
from contractor.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

def loginpage(request):
    return render(request, 'loginpage.html')

def loginaction(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if name == 'admin' and password == 'admin':
            data = Usermodel.objects.all()
            return render(request, 'admins/adminhome.html', {'data': data})

        try:
            if user_type == 'user':
                user = Usermodel.objects.get(username=name, password=password)
                if user.is_active:
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['user_type'] = 'user'

                    user_id = request.session.get('user_id')
                    user = Usermodel.objects.get(id=user_id)
    
                    context = {
                        'user': user,
                    }
            
                    return render(request, 'user/userhome.html', context)
                else:
                    message = 'User not activated, contact admin.'
                    return render(request, 'loginpage.html', {'message': message})
            elif user_type == 'contractor':
                contractor = Contractormodel.objects.get(username=name, password=password)
                if contractor.is_active:
                    request.session['user_id'] = contractor.id
                    request.session['username'] = contractor.username
                    request.session['user_type'] = 'contractor'

                    user_id = request.session.get('user_id')
                    user = Contractormodel.objects.get(id=user_id)
    
                    context = {
                        'user': user,
                    }

                    return render(request, 'contractor/contractorhome.html', context)
                else:
                    message = 'Contractor not activated, contact admin.'
                    return render(request, 'loginpage.html', {'message': message})
        except Usermodel.DoesNotExist:
            message= 'User does not exist.'
            return render(request, 'loginpage.html', {'message': message})
        except Contractormodel.DoesNotExist:
            message= 'Contractor does not exist.'
            return render(request, 'loginpage.html', {'message': message})

    return render(request, 'loginpage.html')

def user_registration_page(request):
    return render(request, 'userregisterpage.html')

def contractor_registration_page(request):
    return render(request, 'contractorregisterpage.html')

def logout(request):
    return render(request, 'loginpage.html')