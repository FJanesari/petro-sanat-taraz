from django.contrib import admin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm
from .models import ContactUsInfo, ContactMessage, AboutUsInfo, AboutUsPost, Setting, HomeInfo, FanFact
from .forms import SingleActiveInstanceMixin


admin.site.site_header = 'پنل ادمین پترو صنعت تاراز'
admin.site.site_title = 'پترو صنعت تاراز'
admin.site.index_title = 'به پنل ادمین پترو صنعت تاراز خوش آمدید!'


class SettingAdminForm(SingleActiveInstanceMixin, TranslatableModelForm):
    model_class = Setting
    active_field_name = "is_active"

    class Meta:
        model = Setting
        fields = "__all__"


@admin.register(Setting)
class SettingAdmin(TranslatableAdmin):
    form = SettingAdminForm
    readonly_fields = ('created_at', 'updated_at')
    list_display = ("site_title", "mobile_number", "telephone", "email", "is_active")
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            "fields": ("site_title", "address", "footer_text", "link_title_one", "link_title_two")
        }),
        ("عمومی", {
            "fields": ("link_address_one", "link_address_two", "logo", "mobile_number", "telephone", "email", "instagram", "linkedin", "telegram", "is_active")
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


class ContactInfoAdminForm(SingleActiveInstanceMixin, TranslatableModelForm):
    model_class = ContactUsInfo
    active_field_name = "is_active"

    class Meta:
        model = ContactUsInfo
        fields = "__all__"


@admin.register(ContactUsInfo)
class ContactUsInfoAdmin(TranslatableAdmin):
    form = ContactInfoAdminForm
    list_display = ('__str__', 'email', 'phone', "is_active")
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'meta_title', 'meta_description',
                'page_title_one', 'description_one',
                'page_title_two', 'description_two',
                'address', 'phone', 'phone_two', 'phone_three', 'phone_four',
                'post_code', 'fax'
            )
        }),
        ("عمومی", {
            'fields': (
                'email', "is_active", 'meta_robots'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'subject', 'message')
    readonly_fields = ('created_at',)


class AboutAdminForm(SingleActiveInstanceMixin, TranslatableModelForm):
    model_class = AboutUsInfo
    active_field_name = "is_active"

    class Meta:
        model = AboutUsInfo
        fields = "__all__"


@admin.register(AboutUsInfo)
class AboutUsInfoAdmin(TranslatableAdmin):
    form = AboutAdminForm
    list_display = ("__str__", "is_active", "created_at")
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'meta_title', 'meta_description',
                'banner_title', 'banner_description',
                'title', 'content',
            )
        }),
        ("عمومی", {
            'fields': (
                "video", "is_active", 'meta_robots'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(AboutUsPost)
class AboutUsPostAdmin(TranslatableAdmin):
    list_display = ("__str__", "is_active", "created_at")
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'post_title', 'post_content',
            )
        }),
        ("عمومی", {
            'fields': (
                "is_active", "image", "slug"
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


class HomeAdminForm(SingleActiveInstanceMixin, TranslatableModelForm):
    model_class = HomeInfo
    active_field_name = "is_active"

    class Meta:
        model = HomeInfo
        fields = "__all__"


@admin.register(HomeInfo)
class HomeInfoAdmin(TranslatableAdmin):
    form = HomeAdminForm
    list_display = ("__str__", "is_active", "created_at")
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'meta_title', 'meta_description',
                'banner_title', 'banner_description',
                'title', 'content',
            )
        }),
        ("عمومی", {
            'fields': (
                "is_active", "image", 'meta_robots'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(FanFact)
class FanFactAdmin(TranslatableAdmin):
    list_display = ("__str__", "is_active", "created_at")
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'card_title', 'card_content',
            )
        }),
        ("عمومی", {
            'fields': (
                "is_active",
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
