from home_app.models import *
from shopping_app.models import *
from django import template




register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated :
        qs = Cart.objects.filter(user=user , ordered=False)
        if qs.exists() :
            return qs[0].items.count()
    return 0