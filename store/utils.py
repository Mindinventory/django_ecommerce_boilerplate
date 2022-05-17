import json

from store.models import Product
from ecommerce import logger


# Create a cookie for managing cookie items
def cookiecart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except Exception as ex:
        print(ex.args)
        cart = {}

    items = []
    gst = 0
    cartitems = 0
    s_total = 0
    sub_total = 0

    for i in cart:
        try:
            cartitems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            gst_one = "{:.1f}".format(total * (18 / 100))
            item_total = float(total) + float(gst_one)
            gst += float(gst_one)
            s_total += item_total
            sub_total = format(s_total, '.1f')

            item = {'product': {'id': product.id, 'name': product.name, 'price': product.price, 'image': product.image},
                    'quantity': cart[i]["quantity"], 'get_total': total}
            items.append(item)
        except Exception as ex:
            logger.info(ex.args)
            pass

    return {'items': items, 'gst': gst, 'sub_total': sub_total, 'cartitems': cartitems}
