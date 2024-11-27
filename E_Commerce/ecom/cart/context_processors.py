from .cart import Cart

#create context processor so card can work on all pages of site
def cart(request):
    #return default data from card
    return {'cart': Cart(request)}