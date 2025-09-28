import os
import django

# 1. Set settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ValueTech.settings")

# 2. Setup Django
django.setup()

# 3. Now import models
from store.models import Product, ProductCategory

# Example usage
for product in Product.objects.all():
    print("Product ",product.name)

for category in ProductCategory.objects.all():
    print("Category ",category.category)
