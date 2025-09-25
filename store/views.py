from django.db.models import F, ExpressionWrapper, IntegerField, FloatField
from django.shortcuts import render, get_object_or_404
from store.models import Product, Category, subCategory, typesOfSubCategory

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


def category_view(request):
    categories = Category.objects.all().prefetch_related('subcategory_set__typesofsubcategory_set')
    return render(request, 'base.html', {"categories": categories})


def product_list(request, slug=None):
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

    selected_category = None
    selected_subcategory = None
    selected_type = None

    # if category:  # filter only if a category is passed
    #
    #     # View All Latest Gadgets
    #     if category == 'Latest Gadgets':
    #         products = products.filter(category__name="Gadget")  # show all gadgets from gadget category
    #     elif category == 'New Arrival':
    #         products = products
    #     else:
    #         products = products.filter(category__name__iexact=category)

    if slug:    # filter only if a category slug is passed
        # Special filter: latest-gadgets = show all latest gadgets
        if slug == 'latest-gadgets':
            products = products.filter(category__name="Gadget")  # show all gadgets from gadget category

        else:
            # Try matching Category
            try:
                selected_category = Category.objects.get(slug=slug)
                products = products.filter(category=selected_category)
            except Category.DoesNotExist:
                pass

            # Try matching SubCategory
            if not products.exists():
                try:
                    selected_subcategory = subCategory.objects.get(slug=slug)
                    products = products.filter(category=selected_subcategory.category,
                                               category__subcategory=selected_subcategory)
                except subCategory.DoesNotExist:
                    pass

            # Try matching Type
            if not products.exists():
                try:
                    selected_type = typesOfSubCategory.objects.get(slug=slug)
                    products = products.filter(category=selected_type.category,
                                               category__subcategory=selected_type.sub_category)
                except typesOfSubCategory.DoesNotExist:
                    pass

    context = {
        'products': products,
        'slug': slug,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'selected_type': selected_type,
    }
    return render(request, 'store/products.html', context)


def new_arrival_products(request):
    # New Arrival = show all products
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
    return render(request, "store/products.html", {
        "products": products,
        "category_name": "New Arrival",
    })


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    extra_images = product.images.all()  # all related ProductImage

    # --- Related Products ---
    related_products = (
        Product.objects
        .filter(category=product.category)
        .exclude(slug=product.slug)
        .order_by('-product_adding_date')[:4]  # newest first, Limit to 4 products
    )

    # --- Recently Viewed Tracking ---
    recently_viewed = request.session.get("recently_viewed", [])

    # always move the current product to the front
    if slug not in recently_viewed:
        recently_viewed.insert(0, slug)  # add current slug at start

    # Save back to session (keep more than 4, so we can exclude current later)
    request.session["recently_viewed"] = recently_viewed[:10]
    request.session.modified = True

    # --- Exclude current product from recently viewed list & limit to 4 others ---
    recently_viewed_products = get_recently_viewed(request, exclude_slug=slug, limit=4)

    context = {
        "product": product,
        "extra_images": extra_images,
        "colors": product.colors.all(),
        "sizes": product.sizes.all(),
        "related_products": related_products,
        "recently_viewed": recently_viewed_products,  # ordered helper
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

