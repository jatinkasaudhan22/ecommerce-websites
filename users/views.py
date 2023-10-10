from django.shortcuts import render
import users.views as views
# Create your views here.
def home(request):
    return render(request, template_name= "index.html")


def user_login(request):
   return render(request, template_name= "login.html")


def user_register(request):
    return render(request, template_name= "register.html")

def user_profile(request):
    return render(request, template_name= "profile.html")