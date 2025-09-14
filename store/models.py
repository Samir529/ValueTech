from django.db import models
from django.utils.text import slugify


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
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
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
    color = models.CharField(max_length=100, blank=True, null=True)
    specification = models.TextField()
    description = models.TextField()

    # Warranty
    warranty = models.CharField(max_length=100, default='1 Year')
    warranty_details = models.TextField(blank=True, null=True)

    # Product Image
    product_image = models.ImageField(
        upload_to="Products/",
        default="/media/Products/no-image-available-icon-vector.JPG",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

