from django.db.models import F, ExpressionWrapper, IntegerField, FloatField
from django.shortcuts import render, get_object_or_404
from store.models import Product, Category, subCategory, brandsOrTypesOfSubCategory

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
    latest_gadgets = annotated_qs.filter(categories__name="Gadget")[:20]  # show latest 20 gadgets from gadget category
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
    products = None
    selected_category = None
    selected_sub_category = None
    selected_brand_or_type = None

    if slug:    # filter only if a category slug is passed

        # Special filter: latest-gadgets = show all latest gadgets
        if slug == 'latest-gadgets':
            products = Product.objects.filter(categories__name="Gadget")  # show all gadgets from gadget category

        else:
            # Try matching SubCategory first
            try:
                selected_sub_category = subCategory.objects.get(slug=slug)
                products = Product.objects.filter(sub_categories=selected_sub_category)
            except subCategory.DoesNotExist:
                # If not sub_category, try matching brand_or_type
                try:
                    selected_brand_or_type = brandsOrTypesOfSubCategory.objects.get(slug=slug)
                    products = Product.objects.filter(brands_or_types=selected_brand_or_type)
                except brandsOrTypesOfSubCategory.DoesNotExist:
                    # Finally try matching Category
                    try:
                        selected_category = Category.objects.get(slug=slug)
                        products = Product.objects.filter(categories=selected_category)
                    except Category.DoesNotExist:
                        pass
    else:
        products = Product.objects.all()

    if products is not None:
        products = (
            products
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

    context = {
        'products': products,
        'slug': slug,
        'selected_category': selected_category,
        'selected_sub_category': selected_sub_category,
        'selected_brand_or_type': selected_brand_or_type,
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

    # --- Breadcrumb categories ---
    # 1. From query param (if clicked via category page)
    current_category = None
    cat_slug = request.GET.get("categories")
    if cat_slug:
        current_category = Category.objects.filter(slug=cat_slug).first()

    # 2. Fallback to primary_category or first assigned category
    if not current_category:
        current_category = product.primary_category or product.categories.first()

    current_sub_category = None
    sub_cat_slug = request.GET.get("sub_categories")
    if sub_cat_slug:
        current_sub_category = subCategory.objects.filter(slug=sub_cat_slug).first()

    # 2. Fallback to primary_sub_category or first assigned category
    if not current_sub_category:
        current_sub_category = product.primary_sub_category or product.sub_categories.first()  # assuming ManyToManyField to subCategory


    # --- Related Products ---
    related_products = (
        Product.objects
        .filter(categories__in=product.categories.all())
        .exclude(slug=product.slug)  # exclude the current product
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
        "current_category": current_category,
        "current_sub_category": current_sub_category,
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


def product_variants_json(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.prefetch_related('attribute_values__attribute', 'color_stocks__color')
    out = []
    for v in variants:
        attrs = {av.attribute.name: av.value for av in v.attribute_values.all()}
        colors = [{'id': cs.color.id, 'name': cs.color.color_name, 'code': cs.color.color_code, 'stock': cs.stock} for cs in v.color_stocks.all()]
        out.append({'id': v.id, 'sku': v.sku, 'attributes': attrs, 'colors': colors, 'price': str(v.get_price())})
    return JsonResponse({'variants': out})


def admin_get_categories_and_subcategories(request):
    cat_id = request.GET.get('cat_id')
    if not cat_id:
        return JsonResponse({'results': []})
    subs = list(subCategory.objects.filter(category_id=cat_id).values('id', 'name'))
    return JsonResponse({'results': subs})

