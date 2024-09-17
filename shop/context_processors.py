# your_app/context_processors.py

from .models import Order

def order_list_for_user(request):
    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(Client__user=user, active = True)
        cost = 0
        for i in orders:
            cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
        return {'order_list_for_user': orders, 'total':  round(cost, 2)}
    return {'order_list_for_user': None}
