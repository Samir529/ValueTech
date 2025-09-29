# backup_all_products_except_selected.py
import os
import django
import json

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ValueTech.settings")  # replace with your settings
django.setup()

from store.models import (
    Product,
    ProductCategory,
    ProductImage,
    ProductColor,
    ProductSize,
    Variant,
    VariantColorStock,
)

# --- CONFIGURE SLUGS TO EXCLUDE ---
EXCLUDE_SLUGS = [
    "tyry",
    "ghgh",
    "pny",
    "ererer",
    "ccccccccccccccc",
    "bbbb",
    "dfgfg",
]

# python manage.py dbshell
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'dfgfg';
#
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'bbbb';
#
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'ccccccccccccccc';
#
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'ererer';
#
#
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'pny';
#
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'ghgh';
#
# DELETE FROM store_product_brands_or_types
# WHERE product_id = 'tyry';


backup_data = []

# Fetch all products except excluded ones
products = Product.objects.exclude(slug__in=EXCLUDE_SLUGS)

for product in products:
    print(f"Backing up product: {product.name}")

    # --- Product ---
    backup_data.append({
        "model": "store.product",
        "pk": product.pk,
        "fields": {
            "name": product.name,
            "slug": product.slug,
            "primary_category": product.primary_category.pk if product.primary_category else None,
            "primary_sub_category": product.primary_sub_category.pk if product.primary_sub_category else None,
            "primary_brand_or_type": product.primary_brand_or_type.pk if product.primary_brand_or_type else None,
            "regular_price": str(product.regular_price),
            "special_price": str(product.special_price) if product.special_price else None,
            "stock": product.stock,
            "status": product.status,
            "product_code": product.product_code,
            "brand": product.brand,
            "model": product.model,
            "specification": product.specification,
            "description": product.description,
            "warranty": product.warranty,
            "warranty_details": product.warranty_details,
            "product_image": product.product_image.name if product.product_image else None,
        }
    })

    # --- ProductCategory ---
    for pc in product.productcategory_set.all():
        backup_data.append({
            "model": "store.productcategory",
            "pk": pc.pk,
            "fields": {
                "product": pc.product.pk,
                "category": pc.category.pk if pc.category else None,
                "sub_category": pc.sub_category.pk if pc.sub_category else None,
                "brand_or_type": pc.brand_or_type.pk if pc.brand_or_type else None,
                "created_at": pc.created_at.isoformat(),
            }
        })

    # --- ProductImage ---
    for img in product.images.all():
        backup_data.append({
            "model": "store.productimage",
            "pk": img.pk,
            "fields": {
                "product": img.product.pk,
                "image": img.image.name,
            }
        })

    # --- ProductColor ---
    for color in product.colors.all():
        backup_data.append({
            "model": "store.productcolor",
            "pk": color.pk,
            "fields": {
                "product": color.product.pk,
                "color_name": color.color_name,
                "color_code": color.color_code,
            }
        })

    # --- ProductSize ---
    for size in product.sizes.all():
        backup_data.append({
            "model": "store.productsize",
            "pk": size.pk,
            "fields": {
                "product": size.product.pk,
                "size": size.size,
            }
        })

    # --- Variant & VariantColorStock ---
    for variant in product.variants.all():
        backup_data.append({
            "model": "store.variant",
            "pk": variant.pk,
            "fields": {
                "product": variant.product.pk,
                "sku": variant.sku,
                "attribute_values": [av.pk for av in variant.attribute_values.all()],
                "created_at": variant.created_at.isoformat(),
            }
        })

        for cs in variant.color_stocks.all():
            backup_data.append({
                "model": "store.variantcolorstock",
                "pk": cs.pk,
                "fields": {
                    "variant": cs.variant.pk,
                    "color": cs.color.pk,
                    "stock": cs.stock,
                }
            })

# --- Save to JSON ---
output_file = "backup_all_except_selected.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(backup_data, f, indent=4)

print(f"\n✅ Backup completed! Saved to '{output_file}'")
