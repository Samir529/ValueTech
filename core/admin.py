import nested_admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django import forms
from django.http import JsonResponse
from django.urls import path

# Register models here.
from core.models import customUser
from accounts.models import accountInfo
from offers.models import Offer
from orders.models import Order, OrderItem
from store.models import Product, Category, subCategory, ProductImage, ProductColor, ProductSize, \
    VariantColorStock, Variant, Attribute, AttributeValue, brandsOrTypesOfSubCategory, ProductCategory
from core.forms import VariantForm
from store.forms import CategoryBulkAddForm, SubCategoryBulkAddForm, BrandsOrTypesOfSubCategoryBulkAddForm

admin.site.site_header = 'ValueTech admin'
admin.site.site_title = 'ValueTech admin'
admin.site.index_title = 'ValueTech administration'



class CustomUserAdmin(UserAdmin):
    model = customUser
    save_as = True

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
    extra = 1    # show 1 empty form by default
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 70px; height: 70px; object-fit: cover;" />',
                               obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


class ProductColorInline(nested_admin.NestedTabularInline):
    model = ProductColor
    extra = 1


class ProductSizeInline(nested_admin.NestedTabularInline):
    model = ProductSize
    extra = 1



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



class ProductCategoryInline(nested_admin.NestedTabularInline):
    model = ProductCategory
    extra = 1
    # autocomplete_fields = ["category", "sub_category", "brand_or_type"]


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    model = Product
    readonly_fields = ["image_preview"]
    save_as = True  # adds "Save as new" button

    # list_display = ("name", "category", "brand", "product_adding_date", "status", "product_code")
    list_display = ("name", "get_categories", "get_sub_categories", "stock", "status", "image_preview")
    prepopulated_fields = {"slug": ("name",)}  # auto fill slug from name
    # filter_horizontal = ("categories", "sub_categories", "brands_or_types")
    inlines = [ProductCategoryInline, ProductImageInline, ProductColorInline, ProductSizeInline, VariantInline]

    list_filter = ("status", "categories", "sub_categories", "brands_or_types")
    fieldsets = (
        (None, {"fields": ("primary_category", "primary_sub_category", "primary_brand_or_type", "name", "slug",
                           "product_code", "product_adding_date", "brand", "model", "regular_price", "special_price",
                           "status", "stock", "specification", "description", "warranty", "warranty_details",
                           "product_image", "image_preview")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("primary_category", "primary_sub_category", "primary_brand_or_type", "name", "slug",
                       "product_code", "product_adding_date", "brand", "model", "regular_price", "special_price",
                       "status", "stock", "specification", "description", "warranty", "warranty_details",
                       "product_image")}
         ),
    )
    search_fields = ("name", "product_code", "sub_categories")
    ordering = ("-product_adding_date",)


    def image_preview(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover;" />',
                obj.product_image.url
            )
        return "-"
    image_preview.short_description = "Preview"


    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = "Categories"

    def get_sub_categories(self, obj):
        return ", ".join([sc.name for sc in obj.sub_categories.all()])
    get_sub_categories.short_description = "Sub Categories"

    def get_brands_or_types(self, obj):
        return ", ".join([bt.name for bt in obj.brands_or_types.all()])
    get_brands_or_types.short_description = "Brands or Types"



admin.site.register(customUser, CustomUserAdmin)


# Generic base admin with save_as enabled
class SaveAsAdmin(admin.ModelAdmin):
    save_as = True  # applies "Save as new" globally


@admin.register(accountInfo)
class AccountInfoAdmin(SaveAsAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(SaveAsAdmin):
    form = CategoryBulkAddForm
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)  # required for autocomplete_fields


@admin.register(subCategory)
class SubCategoryAdmin(SaveAsAdmin):
    form = SubCategoryBulkAddForm
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "category__name")


@admin.register(brandsOrTypesOfSubCategory)
class BrandsOrTypesOfSubCategoryAdmin(SaveAsAdmin):
    form = BrandsOrTypesOfSubCategoryBulkAddForm
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "sub_category__name")


@admin.register(ProductImage)
class ProductImageAdmin(SaveAsAdmin):
    pass


@admin.register(ProductColor)
class ProductColorAdmin(SaveAsAdmin):
    pass


@admin.register(ProductSize)
class ProductSizeAdmin(SaveAsAdmin):
    pass


@admin.register(Order)
class OrderAdmin(SaveAsAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(SaveAsAdmin):
    pass


@admin.register(Offer)
class OfferAdmin(SaveAsAdmin):
    readonly_fields = ["image_preview"]
    save_as = True  # adds "Save as new" button

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


