from django.db.models import F, ExpressionWrapper, IntegerField, FloatField, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from store.models import Product, Category, subCategory, brandsOrTypesOfSubCategory
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
    # Take the first 15 gadgets
    latest_gadgets = annotated_qs.filter(categories__name="Gadget")[:15]  # show latest 15 gadgets from gadget category
    # latest_gadgets = products[:15]  # show latest 15 products

    context = {
        'products': products,
        'latest_gadgets': latest_gadgets
    }
    return render(request, 'store/home.html', context)


def base(request):
    return render(request, 'base.html')


def coming_soon(request):
    return render(request, "store/coming_soon.html")


def ajax_live_search(request):
    query = request.GET.get("search_field", "").strip()
    results = []

    if query:
        # Search in products (name, brand, model, specification, description, product_code)
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(specification__icontains=query) |
            Q(description__icontains=query) |
            Q(product_code__icontains=query)
        ).distinct()[:5]   # Limit results

        for product in products:
            results.append({
                "type": "product",
                "name": product.name,
                "url": reverse("product_details", args=[product.slug]),  # generates /store/product/<slug>/
                # "image": product.image_url
                "image": product.product_image.url if product.product_image else "/static/assets/images/Default images/product-icon.png",
                "regular_price": str(product.regular_price),
                "special_price": str(product.special_price) if product.special_price else None
            })

        # Search in categories
        categories = Category.objects.filter(name__icontains=query)[:5]
        for cat in categories:
            results.append({
                "type": "category",
                "name": f"Category: {cat.name}",
                "url": reverse("product_list_by_category", args=[cat.slug]),
                "image": cat.image.url if hasattr(cat, 'image') and cat.image else "/static/assets/images/Default images/category-icon.png"
            })

        # Search in sub categories
        sub_categories = subCategory.objects.filter(name__icontains=query)[:5]
        for sub in sub_categories:
            results.append({
                "type": "sub_category",
                "name": f"Sub Category: {sub.name}",
                "url": reverse("product_list_by_subcategory", args=[sub.slug]),
                "image": sub.image.url if hasattr(sub, 'image') and sub.image else "/static/assets/images/Default images/category-icon.png"
            })

        # Search in brands or types of sub categories
        brands_or_types = brandsOrTypesOfSubCategory.objects.filter(name__icontains=query)[:5]
        for brand_or_type in brands_or_types:
            results.append({
                "type": "brand_or_type",
                "name": f"Brand/Type: {brand_or_type.name}",
                "url": reverse("product_list_by_type", args=[brand_or_type.slug]),
                "image": brand_or_type.image.url if hasattr(brand_or_type, 'image') and brand_or_type.image else "/static/assets/images/Default images/category-icon.png"
            })

    return JsonResponse({"results": results})


def search_products(request):
    query = request.GET.get("search_field", "").strip()

    if not query:
        # fallback
        return render(request, "store/products.html", {
            "products": Product.objects.none(),  # empty queryset
            "search_query": query,  # <-- empty string ""
            "search_performed": True,
            "no_search_result_message": "There is no product that matches the search criteria."
        })

    # 1 Try exact product match first
    try:
        product = Product.objects.get(
            Q(name__iexact=query) | Q(slug__iexact=query) | Q(product_code__iexact=query)
        )
        return redirect("product_details", slug=product.slug)
    except Product.DoesNotExist:
        pass

    # 2 If not a product, check for category/subcategory match
    category = Category.objects.filter(name__iexact=query).first()
    if category:
        url = reverse("product_list_by_category", args=[category.slug])
        return redirect(f"{url}?search_query={query}")

    sub_category = subCategory.objects.filter(name__iexact=query).first()
    if sub_category:
        url = reverse("product_list_by_category", args=[sub_category.slug])
        return redirect(f"{url}?search_query={query}")

    brand_or_type = brandsOrTypesOfSubCategory.objects.filter(name__iexact=query).first()
    if brand_or_type:
        url = reverse("product_list_by_category", args=[brand_or_type.slug])
        return redirect(f"{url}?search_query={query}")

    # 3 Otherwise, show normal product list (partial match search)
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(specification__icontains=query) |
        Q(description__icontains=query)
    ).distinct()

    if not products.exists():   # Returns False because QuerySet is empty here
        no_search_result_message = "There is no product that matches the search criteria."
    else:
        no_search_result_message = None

    return render(request, "store/products.html", {
        "products": products,
        "search_query": query,
        "search_performed": True,  # tells template a search was done
        "no_search_result_message": no_search_result_message,
    })


def product_list(request, slug=None):
    products = None
    selected_category = None
    selected_sub_category = None
    selected_brand_or_type = None

    search_query = request.GET.get("search_query", "").strip()  # detect if came from search

    if slug:    # filter only if a category slug is passed

        # Special filter: latest-gadgets = show all latest gadgets
        if slug == 'latest-gadgets':
            products = Product.objects.filter(categories__name="Gadget")  # show all gadgets from gadget category

        else:
            # Try matching SubCategory first
            try:
                selected_sub_category = subCategory.objects.get(slug=slug)
                products = Product.objects.filter(sub_categories=selected_sub_category).distinct()
            except subCategory.DoesNotExist:
                # If not sub_category, try matching brand_or_type
                try:
                    selected_brand_or_type = brandsOrTypesOfSubCategory.objects.get(slug=slug)
                    products = Product.objects.filter(brands_or_types=selected_brand_or_type).distinct()
                except brandsOrTypesOfSubCategory.DoesNotExist:
                    # Finally try matching Category
                    try:
                        selected_category = Category.objects.get(slug=slug)
                        products = Product.objects.filter(categories=selected_category).distinct()
                    except Category.DoesNotExist:
                        pass
    else:
        products = Product.objects.all()

    if products.exists():   # Returns True because QuerySet is not empty here
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
        'search_query': search_query,
        'search_performed': bool(search_query),  # True if search_query exists
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
        .filter(sub_categories__in=product.sub_categories.all())
        .exclude(slug=product.slug)  # exclude the current product
        .order_by('-product_adding_date')   # newest first
        .distinct()[:4]   # avoid duplicates, Limit to 4 products
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

