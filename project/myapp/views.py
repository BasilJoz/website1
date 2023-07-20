from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
# Create your views here.


@never_cache
def index(request):
    return render(request, 'index.html')


@never_cache
def handlelogin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/Adm')
        else:
            return redirect('/index')

    if request.method == "POST":
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        myuser = authenticate(username=uname, password=pass1)
        if myuser:
            if myuser.is_superuser:
                login(request, myuser)
                return redirect('Adm')
            else:
                login(request, myuser)
                return redirect('/index')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')
    return render(request, 'login.html')


@never_cache
def handlesignup(request):
    if request.user.is_authenticated:
        return redirect('/index')
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        conformpassword = request.POST.get("pass2")
        # print(uname,email,password,conformpassword)
        if password != conformpassword:
            messages.warning(request, "Password is Incorrect")
            return redirect('/')
        try:
            if User.objects.get(username=uname):
                messages.info(request, "User Name is Taken")
                return redirect('/')

        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request, "Email is Taken")
                return redirect('/')
        except:
            pass

        myuser = User.objects.create_user(uname, email, password)
        myuser.save()
        messages.success(request, "Signup is success Please Login!")
        return redirect('/login')
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return render(request, "signup.html")


@never_cache
def handlelogout(request):
    logout(request,)
    messages.info(request, 'Logout Sucess')
    return redirect("/login")


def Adm(request):
    data = User.objects.all()
    context = {"data": data}
    return render(request, 'adm.html', context)


def insertData(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        query = User.objects.create_user(
            username=username, email=email, password=password)
        query.save()
    data = User.objects.all()
    context = {"data": data}
    return render(request, 'Adm.html', context)


def updateDate(request, id):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        edit = User.objects.get(id=id)
        edit.username = name
        edit.email = email
        edit.save()
        return redirect(Adm)
    data = User.objects.get(id=id)
    context = {"d": data}
    return render(request, 'edit.html', context)


def deleteData(request, id):
    data = User.objects.get(id=id)
    data.delete()
    return redirect(Adm)
