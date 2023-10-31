from django.shortcuts import render, redirect
from orders.models import Cart
from products.models import Products
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.

@login_required
def shopping_cart(request):
    carts = Cart.objects.filter(user_id=request.user.pk).order_by("-created_at")
    has_items = len(carts) > 0
    total_cart_amount = 0
    grand_total = 0
    vat_amount = 0
    if has_items:
        total_cart_amount = sum([cart.cart_total for cart in carts])
        # simple way
        # for item in carts:
        #     total_cart_amount += item.cart_total
        vat_amount = total_cart_amount * 0.13
        grand_total = total_cart_amount + vat_amount
    context = {"carts": carts, "has_items": has_items, "total_cart_amount": total_cart_amount,
               "vat_amount": vat_amount, "grand_total": grand_total}
    return render(request, "carts.html", context)

@login_required
def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    cart_data = {
        "user": request.user,
        "product": product,
        "cart_qty": 1,
        "cart_total": product.price,
    }
    # check if product already exists in cart, if present then update quantity and cart price
    check_cart = Cart.objects.filter(user_id=request.user.pk,
                                     product_id=product_id)
    if check_cart.exists():
        cart = check_cart.first()
        cart.cart_qty += 1
        cart.cart_total = product.price * cart.cart_qty
        cart.save()
    else:
        Cart.objects.create(**cart_data)
    return redirect("/cart")

@login_required
def update_cart(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        # TODO: validate quantity (if quantity is greater than stock)
        cart.cart_qty = quantity
        cart.cart_total = cart.product.price * int(quantity)
        cart.save()
        print("quantity", quantity, cart_id)
    return redirect("/cart")

@login_required
def remove_from_cart(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    cart.delete()
    return redirect("/cart")

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user_id=request.user.pk)
    total = sum([cart.cart_total for cart in cart_items])
    grand_total = total
    context = {"cart_items": cart_items, "grand_total": grand_total, "total": total}
    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")
        city = request.POST.get("city")
        additional_info = request.POST.get("message")
        shipping_type = request.POST.get("shipping_type")
        print("Form Data", shipping_address, city, additional_info, shipping_type)
        shipping_cost = settings.SHIPPING_CHARGES[shipping_type]
        discount = 0
        vat_amount = total * 0.13
        order_data = {
            "user_id": request.user.pk,
            "products": [{"product_id": cart.product_id,
                          "qty": cart.cart_qty,
                          "product_price": cart.product.price,
                          "total": cart.cart_total,
                          "title": cart.product.title,
                          "product_img": cart.product.product_img,
                          } for cart in cart_items],
            "total": grand_total,
            "shipping_address": shipping_address,
            "city": city,
            "additional_info": additional_info,
            "shipping_type": shipping_type,
            "discount": discount,
            "shipping_cost": shipping_cost,
            "vat_amount": vat_amount,
            "grand_total": total + vat_amount + shipping_cost - discount,
        }
        request.session["order_data"] = order_data
        return redirect("/purchase")
    return render(request, "checkout.html", context)

@login_required
def order_summary(request):
    orders = Orders.objects.filter(user_id=request.user.pk).order_by("-created_at")
    order_total = 0
    created_at = None
    order_summary_list = []
    for o in orders:
        products = o.products
        total = o.total
        created_at = o.created_at
        status = o.status
        order_summary_list.append({"products": products,
                                   "total": total,
                                   "id": o.pk,
                                   "created_at": created_at,
                                   "status": status})
        order_total += total
    print("ordered_products", order_summary_list, created_at, order_total)
    context = {"orders": order_summary_list, "order_total": order_total}
    return render(request, "orders.html", context)

@login_required
def purchase_now(request):
    order_data = request.session.get("order_data")
    context = {"order_data": order_data}
    if request.method == "POST":
        # save order data in database
        # cart clear
        Cart.objects.filter(user_id=request)
        print("Purchase Complete")
    return render(request, "purchase.html", context)



def thank_you(request):
    return render(request, template_name="thank-you.html")