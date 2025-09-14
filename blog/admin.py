from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableModelForm
from .models import Article, BlogInfo
from .forms import SingleActiveInstanceMixin
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.exceptions import ValidationError
from django.conf import settings
import bleach


class ArticleAdminForm(TranslatableModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='default'),
        }

    def clean(self):
        cleaned_data = super().clean()

        for lang_code, _ in settings.LANGUAGES:
            field_name = f'content_{lang_code}'
            if field_name in cleaned_data:
                content = cleaned_data[field_name]
                if content:
                    try:
                        cleaned_data[field_name] = self._strict_sanitize(content)
                    except ValueError as e:
                        raise ValidationError(str(e))
        return cleaned_data

    def _strict_sanitize(self, content):
        """پاکسازی مضاعف برای اطمینان"""
        from html import unescape
        decoded = unescape(content)

        # حذف تمام تگ‌های script حتی اگر encode شده باشند
        decoded = decoded.replace('&lt;script', '<script').replace('&lt;/script', '</script')

        # استفاده از bleach برای پاکسازی
        cleaned = bleach.clean(
            decoded,
            tags=[...],  # لیست تگ‌های مجاز
            attributes={...},  # لیست attributeهای مجاز
            strip=True
        )

        # بررسی نهایی
        if '<script' in cleaned.lower():
            raise ValueError("کدهای JavaScript مجاز نیستند!")

        return cleaned


@admin.register(Article)
class ArticleAdmin(TranslatableAdmin):
    form = ArticleAdminForm
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("اطلاعات ترجمه‌پذیر", {
            'fields': (
                'meta_title', 'meta_description',
                'title',
                'content'
            )
        }),
        ("عمومی", {
            'fields': (
                'author', 'image', 'slug', 'canonical_url', 'is_active', 'meta_robots'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


class BlogAdminForm(SingleActiveInstanceMixin, TranslatableModelForm):
    model_class = BlogInfo
    active_field_name = "is_active"

    class Meta:
        model = BlogInfo
        fields = "__all__"


@admin.register(BlogInfo)
class BlogInfoAdmin(TranslatableAdmin):
    form = BlogAdminForm
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
                "is_active", 'meta_robots'
            )
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
