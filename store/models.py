# store/models.py
from django.db import models
from django.utils.text import slugify
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver
from colorfield.fields import ColorField



def unique_slugify(instance, value, slug_field_name="slug"):
    """
    Generates a unique slug for an instance.
    Only checks the model of the instance.
    """
    slug = slugify(value)
    ModelClass = instance.__class__
    unique_slug = slug
    counter = 1

    # Keep generating until unique
    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    serial = models.IntegerField(blank=True, null=True)
    display_at_bar = models.BooleanField(default=False)
    category_adding_date = models.DateTimeField(auto_now_add=True)  # stores full date + time

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)



class subCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)



class typesOfSubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    sub_category = models.ForeignKey(
        subCategory, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Types of Sub Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)



class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")
    sub_category = models.ManyToManyField(subCategory, related_name="products", blank=True)
    types_of_sub_category = models.ManyToManyField(typesOfSubCategory, related_name="products", blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, primary_key=True, blank=True)
    product_adding_date = models.DateTimeField(auto_now_add=True)   # stores full date + time

    # Pricing
    regular_price = models.DecimalField(max_digits=10, decimal_places=0)
    special_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=0)

    # Stock
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("in_stock", "In Stock"),
            ("pre_order", "Pre Order"),
            ("up_coming", "Up Coming"),
            ("out_of_stock", "Out of Stock"),
        ],
        default="in_stock",
    )

    # Product details
    product_code = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    specification = models.TextField()
    description = models.TextField()

    # Warranty
    warranty = models.CharField(max_length=100, default='1 Year')
    warranty_details = models.TextField(blank=True, null=True)

    # Product Image
    product_image = models.ImageField(
        upload_to="Products/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    # Price validation
    def clean(self):
        # Make sure special price < regular price
        if self.special_price is not None and self.special_price >= self.regular_price:
            raise ValidationError({
                "special_price": "Special price must be less than the regular price."
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # <-- call clean() before saving
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.product_image and hasattr(self.product_image, "url"):
            return self.product_image.url
        return static("assets/images/Default images/no-image-available-icon-vector.jpg")



class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="Products/")

    def __str__(self):
        return f"Image for {self.product.name}"



class ProductColor(models.Model):
    product = models.ForeignKey(
        Product, related_name="colors", on_delete=models.CASCADE
    )
    color_name = models.CharField(max_length=50, blank=True, null=True)
    # color_code = models.CharField(max_length=7, blank=True, null=True)  # HEX code (optional)
    color_code = ColorField(max_length=7, blank=True, null=True)  # adds a color picker in admin

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"



class ProductSize(models.Model):
    product = models.ForeignKey(
        Product, related_name="sizes", on_delete=models.CASCADE
    )
    size = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product.name} - {self.size}"



# Delete main product image file from media folder when product is deleted
@receiver(post_delete, sender=Product)
def delete_product_main_image(sender, instance, **kwargs):
    """
    Delete main product image from storage only if
    no other Product is using the same file.
    """
    image = instance.product_image
    if image and image.name:  # check file exists in field
        qs = Product.objects.filter(product_image=image.name)
        if not qs.exists():  # no other product uses it
            image.delete(save=False)



@receiver(post_delete, sender=ProductImage)
def delete_product_gallery_image(sender, instance, **kwargs):
    """
    Delete gallery/extra image from storage only if
    no other ProductImage is using the same file.
    """
    image = instance.image
    if image and image.name:  # file exists
        qs = ProductImage.objects.filter(image=image.name)
        if not qs.exists():  # no other gallery references it
            image.delete(save=False)




class Attribute(models.Model):
    """High-level attribute (Battery, Belt)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class AttributeValue(models.Model):
    """Concrete value for an Attribute (200mah, 300mah, silicone, magnetic)"""
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)

    class Meta:
        unique_together = (('attribute', 'value'),)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.value)
        super().save(*args, **kwargs)


class Variant(models.Model):
    """A product variant defined by a set of AttributeValue(s)."""
    product = models.ForeignKey('Product', related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=120, blank=True, null=True, unique=True)
    attribute_values = models.ManyToManyField(AttributeValue, related_name='variants')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        parts = [f"{av.attribute.name}={av.value}" for av in self.attribute_values.all()]
        return f"{self.product.name} ({', '.join(parts)})" if parts else f"{self.product.name} - variant"


    def get_price(self):
        return self.regular_price or self.product.regular_price


class VariantColorStock(models.Model):
    """Per-variant per-color stock (nested under Variant in admin)."""
    variant = models.ForeignKey(Variant, related_name='color_stocks', on_delete=models.CASCADE)
    # reusing ProductColor model (it references product already)
    color = models.ForeignKey('ProductColor', on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('variant', 'color'),)

    def __str__(self):
        return f"{self.variant} — {self.color.color_name}: {self.stock}"

