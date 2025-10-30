from django.contrib import admin
from django.utils.html import format_html
from .models import Redirect
from urllib.parse import unquote


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ("display_old_path", "display_new_path", "active", "created_at")
    list_editable = ("active",)
    search_fields = ("old_path", "new_path")
    list_filter = ("active", "created_at")
    readonly_fields = ("created_at", "display_decoded_old_path", "display_decoded_new_path")

    fieldsets = (
        (None, {
            'fields': ('old_path', 'new_path', 'active')
        }),
        ('نمایش دیکد شده', {
            'fields': ('display_decoded_old_path', 'display_decoded_new_path'),
            'classes': ('collapse',)
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        from urllib.parse import unquote
        obj.old_path = '/' + unquote(obj.old_path).strip('/')
        obj.new_path = '/' + unquote(obj.new_path).strip('/')
        super().save_model(request, obj, form, change)

    def display_old_path(self, obj):
        return format_html('<code>{}</code><br><small>{}</small>',
                           obj.old_path, unquote(obj.old_path))

    display_old_path.short_description = "آدرس قدیمی"

    def display_new_path(self, obj):
        return format_html('<code>{}</code><br><small>{}</small>',
                           obj.new_path, unquote(obj.new_path))

    display_new_path.short_description = "آدرس جدید"

    def display_decoded_old_path(self, obj):
        return unquote(obj.old_path)

    display_decoded_old_path.short_description = "آدرس قدیمی (دیکد شده)"

    def display_decoded_new_path(self, obj):
        return unquote(obj.new_path)

    display_decoded_new_path.short_description = "آدرس جدید (دیکد شده)"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
