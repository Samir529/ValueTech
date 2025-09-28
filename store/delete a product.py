import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ValueTech.settings")
django.setup()

from store.models import Product

# Get product by name, slug, or ID
product = Product.objects.get(name="tyry")

# Delete all related data first
product.images.all().delete()       # ProductImage
product.colors.all().delete()       # ProductColor
product.sizes.all().delete()        # ProductSize
product.variants.all().delete()     # Variant (cascades to VariantColorStock)
product.productcategory_set.all().delete()  # ProductCategory

# Finally delete the product
product.delete()

print("Product and related objects deleted successfully!")
