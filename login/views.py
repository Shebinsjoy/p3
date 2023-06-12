from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
from login.models import details


# Create your views here.

@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        
        if pass1 == pass2:

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken. Please try some other username')
                return redirect('signup')
            
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'A user already exists on that email address.')
                return redirect('signup')

            else:
                
                my_user = User.objects.create_user(username, email, pass1)
                
                my_user.save()
                
                messages.success(request, 'Your account has been created!.You can log in now.')

                return redirect('signin')
        
        else:
            messages.info(request,"Passwords don't match.Try again.")
            return redirect('signup')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signin(request):

    if 'username' in request.session:
        return redirect(home)

    if request.method == 'POST':

        username = request.POST['uname']
        password = request.POST['password']

        print("Username is",username)

        user = authenticate(username = username, password = password)

        if user is not None:
                request.session['username'] = username
                return redirect(home)
            

            
        else:
            messages.info(request,'Check username or password.')
            print('User does not exist')
            return render(request,'login.html')
    
    return render(request,'login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def home(request):
    if 'username' in request.session:
        temp = {"username":request.session['username']}
        context = {'temp':temp}
        return render(request,'home.html',context)
    return redirect(signin)


@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def signout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect(signin)

# @login_required(login_url='admin')
@cache_control(no_cache=True,must_revalidate=True,no_store=True) 
@never_cache
def dashboard(request):
    if 'admin' in request.session:
        users = User.objects.filter(is_superuser=False).order_by('id')
        context = {
            'users' : users,
        }
        return render(request,'admin.html',context)
    else:
        return redirect('admin')
@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def admin_logout(request):
    if 'admin' in request.session:
        request.session.flush()
    logout(request)
    return redirect('admin')
@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = User.objects.create_user(
            username = name,
            email    = email,
            password = password,
        )
        
        print(user.username)
        return redirect('dashboard')
    
    return render(request,'admin.html')


@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def edit(request):
    det = details.objects.all()

    context = {
        'det' : det,

    }


    return redirect(request,'admin.html',context)

@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def update(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user.username = name
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        return redirect('dashboard')
    else:
        context = {
            'user': user
        }
        return render(request, 'admin.html', context)

@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def delete(request,id):
    det = User.objects.filter(id=id)
    det.delete()

    context ={
        'det':det,

    }
    
    return redirect( 'dashboard')


@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def adminpage(request):
    if 'username' in request.session:
        return redirect('home')
    elif 'admin' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            pass1=request.POST.get('pass')
            User=authenticate(request,username=username,password=pass1)

            if User is not None and User.is_superuser :
                request.session['admin']=username
                login(request,User)
                return redirect('dashboard')
            
            else:
                return HttpResponse("username or password is incorrect")
            

        else:
            
            return render (request,'admin_login.html')



@cache_control(no_cache = True,must_revalidate =True,no_store =True)
def search(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(username__icontains=query)
        print(results)
    else:
        results = []
    context = {
        'users': results,
        'query': query,
    }
    return render(request, 'admin.html', context)










