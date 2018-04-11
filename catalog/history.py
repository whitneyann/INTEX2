from catalog import models as cmod

class lastFiveMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        product_ids = request.session.get('last_five',[])

        products = []

        for i in product_ids:
            products.append(cmod.Product.objects.get(id=i))

        last_five = products
        request.last_five = last_five
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        request.session['last_five'] = []

        for r in request.last_five:

            request.session['last_five'].append(r.id)


        # Code to be executed for each request/response after
        # the view is called.

        return response
