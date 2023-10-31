from django.urls import path
import orders.views as views

urlpatterns = [
    path("cart", views.shopping_cart, name="cart_page"),
    path("checkout", views.checkout, name="checkout_page"),
    path("order-summary", views.order_summary, name="order_summary_page"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("update-cart/<int:cart_id>", views.update_cart, name="update_cart"),
    path("remove-cart/<int:cart_id>", views.remove_from_cart, name="remove_from_cart"),
    path("purchase", views.purchase_now, name="purchase"),
    path("thank-you", views.thank_you, name="")
]