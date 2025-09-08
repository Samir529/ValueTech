# import core
# from store.models import Category, Product
#
#
# @core.register(Category)
# class CategoryAdmin(core.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#
#
# @core.register(Product)
# class ProductAdmin(core.ModelAdmin):
#     list_display = ("name", "category", "price", "stock")
#     prepopulated_fields = {"slug": ("name",)}
#
