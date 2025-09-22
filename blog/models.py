from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django_jalali.db import models as jmodels
from .signals import CleanedCKEditor5Field
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Article(TranslatableModel):
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
        og_title=models.CharField('عنوان OG', max_length=255, blank=True, null=True),
        og_description=models.TextField('توضیحات OG', blank=True, null=True),
        og_image=models.ImageField('عکس OG', upload_to="og_images/", blank=True, null=True),
        title=models.CharField(max_length=255, verbose_name="عنوان"),
        content=CleanedCKEditor5Field(config_name='default', blank=True, verbose_name="محتوای مقاله"),
    )
    author = models.CharField(max_length=100, verbose_name="نویسنده")
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True, verbose_name="تصویر شاخص")
    video = models.FileField('ویدئو',upload_to='videos/', blank=True)
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(800, 600)],
        options={'quality': 80}
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)


class BlogInfo(TranslatableModel):
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
        og_title=models.CharField('عنوان OG', max_length=255, blank=True, null=True),
        og_description=models.TextField('توضیحات OG', blank=True, null=True),
        og_image=models.ImageField('عکس OG', upload_to="og_images/", blank=True, null=True),
        banner_title=models.CharField(max_length=200, verbose_name="عنوان بنر صفحه"),
        banner_description=models.TextField(verbose_name="توضیحات بنر صفحه"),
        title=models.CharField("عنوان", max_length=200, blank=True),
        content=models.TextField("محتوا", blank=True,),
    )
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = " صفحه وبلاگ"
        verbose_name_plural = " صفحه وبلاگ"

    def __str__(self):
        return self.safe_translation_getter('banner_title', any_language=True)
