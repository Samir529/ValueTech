from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import customUser
from accounts.models import accountInfo
# Register your models here.
from store.models import Product, Category


admin.site.site_header = 'ValueTech core'
admin.site.site_title = 'ValueTech core'
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


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("name", "category", "brand", "product_adding_date", "status", "product_code")
    list_filter = ("status", "category", "brand")
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "product_code", "brand", "model", "color", "regular_price",
                           "special_price", "status", "stock", "specification", "description", "warranty",
                           "warranty_details", "product_image")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("category", "name", "slug", "product_code", "product_adding_date", "brand", "model", "color",
                       "regular_price", "special_price", "status", "stock", "specification", "description", "warranty",
                        "warranty_details", "product_image")}
         ),
    )
    search_fields = ("name",)
    # ordering = ("product_adding_date",)


admin.site.register(customUser, CustomUserAdmin)
admin.site.register(accountInfo)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

