from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django_jalali.db import models as jmodels
from .signals import CleanedCKEditor5Field


class Project(TranslatableModel):
    translations = TranslatedFields(
        meta_title=models.CharField("متا تایتل", default='Petro Sanat Taraz'),
        meta_description=models.TextField(' متا دسکریپشن', default='توضیحات سایت'),
        title=models.CharField(max_length=255, verbose_name="عنوان"),
        content=CleanedCKEditor5Field(config_name='default', blank=True, verbose_name="محتوای پروژه"),
    )
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True, verbose_name="تصویر شاخص")
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
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه ها"

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class ProjectInfo(TranslatableModel):
    translations = TranslatedFields(
        meta_title=models.CharField("متا تایتل", default='Petro Sanat Taraz'),
        meta_description=models.TextField(' متا دسکریپشن', default='توضیحات سایت'),
        banner_title=models.CharField(max_length=200, verbose_name="عنوان بنر صفحه"),
        banner_description=models.TextField(verbose_name="توضیحات بنر صفحه"),
        title=models.CharField("عنوان", max_length=200, blank=True),
        content=models.TextField("محتوا", blank=True,),
    )
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = " صفحه پروژه"
        verbose_name_plural = " صفحه پروژه"

    def __str__(self):
        return self.safe_translation_getter('banner_title', any_language=True)
