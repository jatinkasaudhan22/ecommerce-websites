from django.shortcuts import render
from products.models import Products
# Create your views here.
def new_arrival_products(request):
    return render(request, template_name= "new-arrival.html")


def product_detail(request, product_id):
    product = Products.objects.get(id=product_id)
    context = {"product": product}
    return render(request, template_name="product-detail.html", context=context )