# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import userForm
from core.models import customUser
from .models import accountInfo


def account_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                if user.is_staff != True:
                    login(request, user)
                    if not remember_me:     # unchecked
                        request.session.set_expiry(0)   # if exits from browser then login will lost,
                                                        # else, if exits from browser then login will not lost
                    return HttpResponseRedirect(reverse('userPanel'))
                elif user.is_staff == True:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return HttpResponseRedirect(reverse('staffPanel'))
                else:
                    return HttpResponse("No accounts found with this username or password.")
            else:
                return HttpResponse("Account is not active.")
        else:
            messages.error(request, "No match for Email Address or Phone Number and/or Password.")
            return render(request, "accounts/account_login.html")

    return render(request, 'accounts/account_login.html')


@login_required
def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def register_account(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        # heck if email already exists
        if customUser.objects.filter(email=email).exists():
            messages.error(request, "An accounts with this email is already registered!")
            return render(request, "accounts/register_account.html")

        # Check if phone number already exists
        if customUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "An accounts with this phone number is already registered!")
            return render(request, "accounts/register_account.html")

        # If both are unique, save in session and continue
        request.session["first_name"] = request.POST.get("first_name")
        request.session["last_name"] = request.POST.get("last_name")
        request.session["email"] = request.POST.get("email")
        request.session["phone_number"] = request.POST.get("phone_number")
        return redirect("account_password")  # go to password page
    return render(request, "accounts/register_account.html")


def account_password(request):

    if request.method == 'POST':

        user_form = userForm({
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
            'email': request.session.get('email'),
            'phone_number': request.session.get('phone_number'),
            'password': request.POST.get('password'),
            'confirm_password': request.POST.get('confirm_password')
        })

        password = user_form.data['password']
        confirm_password = user_form.data['confirm_password']

        if user_form.is_valid() and password == confirm_password:
            user = user_form.save(commit=False)
            user.set_password(user.password) # hashes the password
            user.save()

            t = accountInfo()
            t.user = user
            t.save()
            # t2 = customUser()
            # t2.username = username
            # t2.password = password
            # t2.first_name = first_name
            # t2.last_name = last_name
            # t2.email = email
            # t2.phone_number = phone_number
            # t2.save()

            # auto login new user
            login(request, user)
            # redirect to user panel
            return redirect('userPanel')

        # Check minimum length of password
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return render(request, "accounts/account_password.html")

        # Check password confirmation
        elif password != confirm_password:
            messages.error(request, "Password confirmation does not match password!")
            return render(request, "accounts/account_password.html")
        else:
            print(user_form.errors)
    else:
        user_form = userForm()
    return render(request, 'accounts/account_password.html', {"form": user_form})


def account(request):
    if request.user.is_authenticated:

        # request.user is the customUser(is the current logged-in user)
        user = request.user
        if user.is_active:
            if user.is_staff != True:
                return HttpResponseRedirect(reverse('userPanel'))
            elif user.is_staff == True:
                return HttpResponseRedirect(reverse('staffPanel'))
            else:
                return HttpResponse("No accounts found with this username or password.")
        else:
            return HttpResponse("Account is not active.")
    else:
        return render(request, 'accounts/account_login.html')


@login_required
def userPanel(request):
    return render(request, 'accounts/user_panel.html')

