from django.shortcuts import render

# Create your views here.
def shopping_cart(request):
    return render(request, template_name="carts.html")

def order_summary(request):
    return render(request, template_name="orders.html")

def checkout(request):
    return render(request, template_name="checkout.html")