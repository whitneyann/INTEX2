from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
import math



#watch beginning of the video. def process_request(request, cat:cmod.Category=None)
# <!--in the left column, make a list from a QUERY-->
# <!--in the top right, have <Page 1 of 4> (the arrows are links, ahrefs)[the 4 would be qry=cmod.Product.objects.all(), then say
# IF, category is not None: then qry=qry.filter(...)]-->
#qry.count()/6  --make sure to round up [this runs a count query on database]
# in the html. <div id="products"></div> (this should be empty! we will load with AJAX into there.)

#in my index.css do #product_list{list-style: none; margin: 0; padding: 0;
##  list tags:::: display: inline-block (makes it like a letter), margin 12px 18px; border 1px solid #CCCCCC; padding: 12px;
        # border-radius: 4px;width:90px; vertical-align: top; min-height: 90px; overflow-y: auto(or scroll); position: relative;}

##product_list > li > .price {position: absolute; right: 0px; top: 0 px; border-radius....background-color....}


@view_function
def process_request(request, cat:cmod.Category=None):

        categoryList=cmod.Category.objects.all()
        productList = cmod.Product.objects.all().filter(status='A')

        if cat is not None:
                productList=cmod.Product.objects.filter(category=cat.id).filter(status='A')

        myPages = math.ceil(productList.count()/6)
        context={
                'categoryList': categoryList,
                'productList': productList,
                'myPages': myPages,
                'name': cat.name if cat is not None else "All Products",
                jscontext("catid"): cat.id if cat is not None else 0,
                jscontext("pagenum"): myPages,

        }

        return request.dmp.render('index.html',
            context,
        )


@view_function
def products(request, cat:cmod.Category=None, pageNumber: int=1):

        productList = cmod.Product.objects.all().filter(status='A').order_by('name')


        if cat is not None:
                productList=cmod.Product.objects.filter(category=cat.id).filter(status='A').order_by('name')

        myPages = math.ceil(productList.count()/6)

        products=[]

        for x in range((pageNumber-1)*6, pageNumber*6):
                if x < len(productList):
                        products.append(productList[x])

        context={
                'products': products,
                'myPages':myPages,
                jscontext("catid"): cat.id if cat is not None else 0,
                jscontext("pagenum"): myPages,
        }

        return request.dmp.render('index.products.html',
                    context
        )
