from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


# Create your views here.


@csrf_exempt
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        newUser = User(username=username, email=email)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)
        messages.success(request, "You have successfully registered!")

        return redirect("index")

    context = {
        "form": form,
    }

    return render(request, "register.html", context)

    ##############################
    # Second way to do it
    # if request.method == "POST":
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         email = form.cleaned_data.get("email")
    #         password = form.cleaned_data.get("password")

    #         newUser = User(username=username, email=email)
    #         newUser.set_password(password)
    #         newUser.save()

    #         login(request, newUser)

    #         return redirect("index")
    #     else:
    #         context = {
    #             "form": form,
    #         }
    #         return render(request, "register.html", context)
    # else:
    #     form = RegisterForm()
    #     context = {
    #         "form": form,
    #     }
    #     return render(request, "register.html", context)


@csrf_exempt
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, "Username or Password is incorrect!")
            return render(request, "login.html", context)

        messages.success(request, "You have successfully logged in!")
        login(request, user)
        return redirect("index")
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect("index")
