# utils.py
from store.models import Product

def get_recently_viewed(request):
    """
    Retrieve recently viewed products from session using product.slug
    """
    product_slugs = request.session.get("recently_viewed", [])
    return Product.objects.filter(slug__in=product_slugs)
