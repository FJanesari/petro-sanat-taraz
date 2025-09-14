from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django_jalali.db import models as jmodels
from .signals import CleanedCKEditor5Field


class Product(TranslatableModel):
    META_ROBOTS_CHOICES = [
        ("index, follow", "Index, Follow (پیشفرض)"),
        ("noindex, follow", "Noindex, Follow"),
        ("index, nofollow", "Index, Nofollow"),
        ("noindex, nofollow", "Noindex, Nofollow"),
    ]
    meta_robots = models.CharField(
        max_length=20,
        choices=META_ROBOTS_CHOICES,
        default="index, follow",
        verbose_name="Meta Robots"
    )
    translations = TranslatedFields(
        meta_title=models.CharField("متا تایتل", default='Petro Sanat Taraz'),
        meta_description=models.TextField(' متا دسکریپشن', default='توضیحات سایت'),
        banner_title=models.CharField(max_length=200, default='محصولات پترو صنعت تاراز', verbose_name="عنوان بنر صفحه"),
        banner_description=models.TextField(blank=True, verbose_name="توضیحات بنر صفحه"),
        title=models.CharField(max_length=255, verbose_name="نام محصول"),
        description=CleanedCKEditor5Field(config_name='default', blank=True, verbose_name="محتوا"),
        price=models.CharField(max_length=100, blank=True, verbose_name="قیمت"),
    )
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True, verbose_name="تصویر")
    slug = models.SlugField("اسلاگ", unique=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class ProductType(TranslatableModel):
    META_ROBOTS_CHOICES = [
        ("index, follow", "Index, Follow (پیشفرض)"),
        ("noindex, follow", "Noindex, Follow"),
        ("index, nofollow", "Index, Nofollow"),
        ("noindex, nofollow", "Noindex, Nofollow"),
    ]
    meta_robots = models.CharField(
        max_length=20,
        choices=META_ROBOTS_CHOICES,
        default="index, follow",
        verbose_name="Meta Robots"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="types",
        verbose_name="محصول"
    )
    translations = TranslatedFields(
        meta_title=models.CharField("متا تایتل", default='Petro Sanat Taraz'),
        meta_description=models.TextField(' متا دسکریپشن', default='توضیحات سایت'),
        banner_title=models.CharField(max_length=200, default='انواع محصولات', verbose_name="عنوان بنر صفحه"),
        banner_description=models.TextField(blank=True, verbose_name="توضیحات بنر صفحه"),
        title=models.CharField(max_length=255, verbose_name="عنوان"),
        description=CleanedCKEditor5Field(config_name='default', blank=True, verbose_name="محتوا"),
    )
    image = models.ImageField(upload_to='products/types/', blank=True, null=True, verbose_name="تصویر شاخص")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصولات"

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class ProductTypeImage(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="gallery"
    )
    image = models.ImageField(upload_to="product-types/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "گالری تصویر نوع محصول"
        verbose_name_plural = "گالری تصاویر نوع محصول"

    def __str__(self):
        return f"تصویر {self.product_type}"


class ProductInfo(TranslatableModel):
    translations = TranslatedFields(
        banner_title=models.CharField(max_length=200, verbose_name="عنوان بنر صفحه"),
        banner_description=models.TextField(verbose_name="توضیحات بنر صفحه"),
    )
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = " صفحه محصولات"
        verbose_name_plural = " صفحه محصولات"

    def __str__(self):
        return self.safe_translation_getter('banner_title', any_language=True)
