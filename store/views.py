from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from store.forms import productForm


def store_home(req):
    products = Product.objects.all().order_by('-product_adding_date')

    # billboard_filter = Product(req.GET, queryset=allPosts)
    context = {'products': products}
    return render(req, 'store/home.html', context)


def base(req):
    return render(req, 'base.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-product_adding_date')
    return render(request, "store/products.html", {"products": products})

def filter_products(request):
    price = request.GET.get("price")
    availability = request.GET.get("availability", "").split(",")
    category = request.GET.get("category")

    products = Product.objects.all()

    if price:
        products = products.filter(price__lte=price)

    if "in_stock" in availability:
        products = products.filter(stock__gt=0)
    if "pre_order" in availability:
        products = products.filter(status="pre_order")
    if "upcoming" in availability:
        products = products.filter(status="upcoming")

    if category and category != "all":
        products = products.filter(category__slug=category)

    html = render_to_string("store/product_grid.html", {"products": products})
    return JsonResponse({"html": html})

