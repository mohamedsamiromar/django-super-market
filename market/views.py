import item
from django.shortcuts import render
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required, user_passes_test

from authentication import permission_roles
from market.form import ProductForm
from market.models import Product, Order, OrderItems


CART_KEY = 'cart'

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@user_passes_test(permission_roles.merchant)
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'product.html', {'products': products})
    elif request.method == 'POST':
        product_new = ProductForm(request.POST)
        if product_new.is_valid():
            product_new.save()
        products = Product.objects.all()
        return render(request, 'product.html', {'form': product_new, 'products': products})



def checkout(request):

    order = Order()
    i = 0
    total_qty = 0
    total_price = 0.0

    while request.POST.get('productId_'+str(i), None) is not None:
        product_id = request.POST.get('productId_'+str(i))
        qty = int(request.POST.get('qty_' + str(i)))
        total_qty = total_qty + qty
        product = Product.objects.get(pk=product_id)
        total_price = total_price + product.price_sale
        product.qty -= qty
        product.save()
        # Handle database
        # 1- Decrease product count (qty) - read from database [[product = Product.objects.get(pk=product_id)]]
        # 2-  Add Entry (row) or (save) in order-item table and order (Create order )
        
        i += 1
    order.total_qty = total_qty
    order.total_price = total_price
    order.save()
    del request.session[CART_KEY]
    return home(request)


def add_to_cart(request):
    if CART_KEY not in request.session:
        request.session[CART_KEY] = []

    if request.method == 'GET':
        return render(request, 'display_cart.html', {'cart_items': request.session['cart']})
    else:
        product_id = request.POST.get('productId')
        product = Product.objects.get(pk=product_id)
        old_items = request.session['cart']
        old_items.append({'product': {'id': product_id, 'title': product.title, 'qty': 1}})
        request.session[CART_KEY] = old_items
        return render(request, 'display_cart.html', {'cart_items': request.session['cart']})


# def save_order(request):
#     if 'cart' in request.session:
#         order = Order(total_qty=0, totla_price=0.0)
#         order.save()
#         for items in request.session['cart']:
#             product = Product.objects.get(pk=items.get('product').get('id'))
#             order.total_qty += product.price_sale
#             order.total.price += item.get('qty')
#             cart_items = OrderItems(product=product, order=order, qty=item.get('qy'))
#             cart_items.save()
#     order.save()
#     request.session.clear()
#     return home(request)


def go_to_order(request):
    order = Order.objects.all()
    return render(request, 'go_to_order.html', {'order': order})


def order_details(request):
    order_id = request.GET.get("orderId")
    order = Order.objects.get(pk=order_id)
    order_items = order.orderitems_set.all()
    return render(request, "order_details.html", {'order': order, 'order_items': order_items})