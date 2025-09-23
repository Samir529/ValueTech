# utils.py
from store.models import Product

def get_recently_viewed(request, exclude_slug=None, limit=4):
    """
    Retrieve recently viewed products from session using product.slug, preserving order.
    Optionally excludes a specific product slug (e.g., the current product). Excludes the given slug (usually current product).
    Always returns up to `limit` products.
    """
    product_slugs = request.session.get("recently_viewed", [])

    # Remove excluded slug if requested / Exclude current product if needed
    if exclude_slug and exclude_slug in product_slugs:
        product_slugs = [s for s in product_slugs if s != exclude_slug]

    # Limit to required count
    product_slugs = product_slugs[:limit]

    # Fetch and sort in session order
    # --- Get Product objects in correct order ---
    recently_viewed_products  = list(Product.objects.filter(slug__in=product_slugs))

    # Sort them according to session order
    recently_viewed_products.sort(key=lambda x: product_slugs.index(x.slug))  # preserve session order

    return recently_viewed_products
