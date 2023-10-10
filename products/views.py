from django.shortcuts import render

# Create your views here.
def new_arrival_products(request):
    return render(request, template_name= "new-arrival.html")


def product_detail(request, product_id):
    return render(request, template_name="product-detail.html")