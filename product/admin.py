from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product, ProductType, ProductTypeImage


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'meta_title', 'meta_description',
                'banner_title', 'banner_description',
                'title',
                'description', 'price'
            )
        }),
        ("عمومی", {
            'fields': (
                'image', 'is_active', 'slug', 'canonical_url'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


class ProductTypeImageInline(admin.TabularInline):
    model = ProductTypeImage
    extra = 1  # تعداد فرم خالی پیش‌فرض
    fields = ["image", "alt_text"]


@admin.register(ProductType)
class ProductTypeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductTypeImageInline]
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'meta_title', 'meta_description',
                'banner_title', 'banner_description',
                'title',
                'description'
            )
        }),
        ("عمومی", {
            'fields': (
                'image', 'product', 'is_active', 'slug', 'canonical_url'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


# class ProductAdminForm(SingleActiveInstanceMixin, TranslatableModelForm):
#     model_class = ProductInfo
#     active_field_name = "is_active"
#
#     class Meta:
#         model = ProductInfo
#         fields = "__all__"
#
#
# @admin.register(ProductInfo)
# class ProductInfoAdmin(TranslatableAdmin):
#     form = ProductAdminForm
#     list_display = ("__str__", "is_active", "created_at")
#     readonly_fields = ('created_at', 'updated_at')
#     fieldsets = (
#         ("اطلاعات ترجمه‌پذیر", {
#             'fields': (
#                 'banner_title', 'banner_description',
#             )
#         }),
#         ("عمومی", {
#             'fields': (
#                 "is_active",
#             )
#         }),
#         ('اطلاعات زمان', {
#             'fields': ('created_at', 'updated_at'),
#         }),
#     )
