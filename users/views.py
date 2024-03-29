from django.shortcuts import render, redirect
from users.forms import RegisterForm, UserRegisterForm
from django.contrib import messages
from users.helper import save_file
from users.models import Profile, User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from products.models import Products
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    sort_by = request.GET.get("sort_by")
    if sort_by:
        request.session["sort_by"] = sort_by  # save sort to user session
    sort_by = request.session.get("sort_by", "-created_at")  # get sort from user session
    # check for search query
    search_query = request.GET.get("query", None)
    print("Search Query: ", search_query)
    if search_query is not None:
        products = Products.objects.filter(title__icontains=search_query).order_by(sort_by)
    else:
        products = Products.objects.all().order_by(sort_by)
    page_size = request.GET.get("per_page", 3)
    paginator = Paginator(products, page_size)  # Show 1 products per page.
    page_number = request.GET.get("page")
    page_data = paginator.get_page(page_number)
    context = {"products": page_data}
    return render(request, "index.html", context)

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("Email: ", email, "Password: ", password)
        check_user = User.objects.filter(email=email)
        if not check_user.exists():
            error = "Account does not exists"
            messages.error(request, error)
            return redirect("/login")
        is_valid_user = authenticate(request, username=check_user[0].username, password=password)
        if is_valid_user is not None:
            login(request, is_valid_user)
            request.session["name"] = is_valid_user.first_name
            return redirect("/profile")
        else:
            error = "Invalid Email or Password"
            messages.error(request, error)
            return redirect("/login")
    return render(request, "login.html")

def user_register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form_data = UserRegisterForm(request.POST)
        if form_data.is_valid():
            print("Form Data: ", form_data.cleaned_data)
            password = form_data.cleaned_data["password"]
            confirm_password = form_data.cleaned_data["confirm_password"]
            if password != confirm_password:
                error = "Password and Confirm Password fields does not match"
                messages.error(request, error)
                return redirect("/register")
            check_user = User.objects.filter(username=form_data.cleaned_data["username"]).exists()
            check_email = User.objects.filter(email=form_data.cleaned_data["email"]).exists()
            if check_user or check_email:
                error = "Username or Email already exists"
                messages.error(request, error)
                return redirect("/register")
            user_account_data = {
                "first_name": form_data.cleaned_data["first_name"], "last_name": form_data.cleaned_data["last_name"],
                "username": form_data.cleaned_data["username"], "email": form_data.cleaned_data["email"],
            }
            user = User.objects.create(**user_account_data)
            user.set_password(password)
            user.save()
            profile_data = {
                "user": user, "contact": form_data.cleaned_data["contact"],
                "address": form_data.cleaned_data["address"], "city": form_data.cleaned_data["city"],
                "profile_pic": "N/A"
            }
            profile = Profile.objects.create(**profile_data)
            return redirect("/login")
        else:
            error = form_data.errors
            messages.error(request, error)
            return redirect("/register")
    return render(request, "register.html", {"form": form})

@login_required
def user_profile(request):
    user_id = request.user.pk   # get user id of logged in user
    # equivalent sql: SELECT * FROM profile WHERE user_id = 1
    # get profile of user with id user_id
    profile = Profile.objects.get(user_id=user_id)
    if request.method == "POST":
        city = request.POST.get("city")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        profile_pic = request.FILES.get("profile_img")
        profile_pic_url = save_file(request, profile_pic)
        print("City: ", city, "Address: ", address, "Contact: ", contact, "Profile Pic: ", profile_pic_url)
        if city != profile.city:
            profile.city = city
        if address != profile.address:
            profile.address = address
        if contact != profile.contact:
            profile.contact = contact
        if profile_pic_url is not None:
            if profile_pic_url != profile.profile_pic:
                profile.profile_pic = profile_pic_url
        profile.save()
        return redirect("/profile")
    # if profile.profile_pic == "N/A":
    #     profile.profile_pic = "https://i.pinimg.com/736x/3f/94/70/3f9470b34a8e3f526dbdb022f9f19cf7.jpg"
    context = {"profile": profile}
    return render(request, "profile.html", context)

def user_logout(request):
    logout(request)
    return redirect("/login")