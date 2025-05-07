from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from authentication.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="GET":
        return render(request,'account.html')
    else:
        email = request.POST['email']
        password = request.POST['password']

        user = user = authenticate(email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'User Not Found .')
        return redirect('/auth/login')
    

def register_view(request):
    if request.method == "GET":
        return render(request, 'account.html')
    
    else:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        dob = request.POST['dob']
        user = User.objects.filter(email = email)
        if user.exists():
            messages.error(request,'Email Already Exists.')
            return redirect('/auth/register')
        
        user = User.objects.create(email=email, first_name = first_name, last_name=last_name, dob=dob)
        user.set_password(password)
        user.save()
        # except:
        #     messages.error(request, 'Something Went Wrong!')
        #     return redirect('/auth/register')
        
        return redirect('/auth/login')

def change_user_credintials(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            return render(request,'components/account-details.html')
        else:
            data = request.POST
            user = User.objects.get(id=request.user.id)
            if 'first_name' in data and data['first_name']:
                user.first_name = data['first_name']
            if 'last_name' in data and data['last_name']:
                user.last_name = data['last_name']
            if 'email' in data and data['email']:
                user.email = data['email']
            try:
                user.save()
            except:
                messages.error(request,'Email Already Exist')
                return redirect('/auth/user/')
            return redirect('/auth/user/')
    else:
        return redirect('auth:login')
            

def change_password(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            data = request.POST
            user = User.objects.get(id=request.user.id)
            if ('c_pass' in data and data['c_pass']) and ('n_pass' in data and data['n_pass']):
                if user.check_password(data['c_pass']):
                    user.set_password(data['n_pass'])
                    user.save()
                    return redirect('/auth/login')
                else:
                    messages.error(request,'Wrong Password!')
                    return redirect('/auth/user/')

                
            else:
                return redirect('/auth/user/')

def logout_view(request):

    logout(request)
    return redirect('/')


def account(request):
    return render(request, 'account.html')


# def recent_tickets(request):
#     context = 

#     return render(request, 'components/recent-tickets.html')