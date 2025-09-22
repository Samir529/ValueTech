from django.db.models import F, ExpressionWrapper, IntegerField, FloatField
from django.shortcuts import render, get_object_or_404
from store.models import Product

from django.http import JsonResponse
from django.template.loader import render_to_string
from store.utils import get_recently_viewed


def store_home(request):
    # Base queryset with annotation
    # All products with discount + discount percentage annotated
    annotated_qs = (
        Product.objects
        .annotate(                              # ORM-powered with annotate(). So I don’t have to loop and calculate inside the view.
            discount=ExpressionWrapper(         # That would be more efficient if I have lots of products. This way the database itself
                F('regular_price') - F('special_price'),    # calculates the discount amount and discount percentage, and my template stays clean.
                output_field=IntegerField()
            ),
            discount_percentage=ExpressionWrapper(
                (F('regular_price') - F('special_price')) * 100.0 / F('regular_price'),
                output_field=FloatField()
            )
        )
        .order_by('-product_adding_date')
    )

    # Take the first 20 products
    products = annotated_qs[:20]

    # Latest Gadgets
    # Take the first 20 gadgets
    latest_gadgets = annotated_qs.filter(category__name="Gadget")[:20]  # show latest 20 gadgets from gadget category
    # latest_gadgets = products[:20]  # show latest 20 products

    context = {
        'products': products,
        'latest_gadgets': latest_gadgets
    }
    return render(request, 'store/home.html', context)


def base(request):
    return render(request, 'base.html')


def product_list(request, category=None):
    products = (
        Product.objects
        .annotate(
            discount=ExpressionWrapper(
                F('regular_price') - F('special_price'),
                output_field=IntegerField()
            ),
            discount_percentage=ExpressionWrapper(
                (F('regular_price') - F('special_price')) * 100.0 / F('regular_price'),
                output_field=FloatField()
            )
        )
        .order_by('-product_adding_date')
    )

    if category:  # filter only if a category is passed

        # View All Latest Gadgets
        if category == 'Latest Gadgets':
            products = products.filter(category__name="Gadget")  # show all gadgets from gadget category
        elif category == 'New Arrival':
            products = products
        else:
            products = products.filter(category__name__iexact=category)

    context = {
        'products': products,
        'selected_category': category,
    }
    return render(request, 'store/products.html', context)


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)

    related_products = (
        Product.objects
        .filter(category=product.category)
        .exclude(slug=product.slug)[:4]  # Limit to 4 products
    )

    # --- Recently Viewed Tracking ---
    recently_viewed = request.session.get("recently_viewed", [])
    if slug not in recently_viewed:
        recently_viewed.insert(0, slug)  # add current slug at start
    # Keep only last 4
    request.session["recently_viewed"] = recently_viewed[:4]
    request.session.modified = True

    context = {
        "product": product,
        "images": product.images.all(),
        "colors": product.colors.all(),
        "sizes": product.sizes.all(),
        "related_products": related_products,
        "recently_viewed": get_recently_viewed(request),
    }
    return render(request, "store/product_details.html", context)


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

