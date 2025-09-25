import nested_admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register models here.
from core.models import customUser
from accounts.models import accountInfo
from offers.models import Offer
from orders.models import Order, OrderItem
from store.models import Product, Category, subCategory, ProductImage, ProductColor, ProductSize, typesOfSubCategory, \
    VariantColorStock, Variant, Attribute, AttributeValue
from core.forms import VariantForm


admin.site.site_header = 'ValueTech admin'
admin.site.site_title = 'ValueTech admin'
admin.site.index_title = 'ValueTech administration'



class CustomUserAdmin(UserAdmin):
    model = customUser
    list_display = ("email", "is_staff", "is_active", "account_creation_date")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "phone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "phone_number", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)



class ProductImageInline(nested_admin.NestedTabularInline):   # or StackedInline
    model = ProductImage
    extra = 3    # show 3 empty form by default
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 70px; height: 70px; object-fit: cover;" />',
                               obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


class ProductColorInline(nested_admin.NestedTabularInline):
    model = ProductColor
    extra = 3


class ProductSizeInline(nested_admin.NestedTabularInline):
    model = ProductSize
    extra = 3



class VariantColorStockInline(nested_admin.NestedTabularInline):
    model = VariantColorStock
    extra = 1
    fields = ('color', 'stock')


class VariantInline(nested_admin.NestedTabularInline):
    model = Variant
    form = VariantForm
    extra = 1
    inlines = [VariantColorStockInline]
    filter_horizontal = ('attribute_values',)
    fields = ('sku', 'attribute_values')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)


@admin.register(Variant)
class VariantAdmin(nested_admin.NestedModelAdmin):
    inlines = [VariantColorStockInline]
    filter_horizontal = ('attribute_values',)
    list_display = ('product', 'sku', 'get_attributes')

    def get_attributes(self, obj):
        return ', '.join([f"{av.attribute.name}:{av.value}" for av in obj.attribute_values.all()])
    get_attributes.short_description = 'Attributes'



class ProductAdmin(nested_admin.NestedModelAdmin):
    model = Product
    readonly_fields = ["image_preview"]

    # list_display = ("name", "category", "brand", "product_adding_date", "status", "product_code")
    list_display = ("name", "category", "brand", "status", "product_code", "image_preview")
    prepopulated_fields = {"slug": ("name",)}  # auto fill slug from name
    inlines = [ProductImageInline, ProductColorInline, ProductSizeInline, VariantInline]

    list_filter = ("status", "category", "brand")
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "product_code", "brand", "model", "regular_price",
                           "special_price", "status", "stock", "specification", "description", "warranty",
                           "warranty_details", "product_image", "image_preview")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("category", "name", "slug", "product_code", "product_adding_date", "brand", "model",
                       "regular_price", "special_price", "status", "stock", "specification", "description",
                       "warranty", "warranty_details", "product_image")}
         ),
    )
    search_fields = ("name",)
    ordering = ("-product_adding_date",)

    def image_preview(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover;" />',
                obj.product_image.url
            )
        return "-"
    image_preview.short_description = "Preview"



admin.site.register(customUser, CustomUserAdmin)



admin.site.register(accountInfo)



admin.site.register(Category)
admin.site.register(subCategory)
admin.site.register(typesOfSubCategory)



admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(ProductSize)



admin.site.register(Order)
admin.site.register(OrderItem)



@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    readonly_fields = ["image_preview"]

    list_display = ("title", "start_date", "end_date", "outlet", "created_at")
    list_filter = ("start_date", "end_date", "outlet")
    search_fields = ("title", "description")
    ordering = ("-created_at",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 400px; height: 400px; object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Offer image"


