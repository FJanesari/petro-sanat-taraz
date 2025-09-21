from django.db import models
from parler.models import TranslatableModel, TranslatedFields
import django_jalali.db.models as jmodels


class Setting(TranslatableModel):
    translations = TranslatedFields(
        site_title=models.CharField(blank=True, verbose_name="عنوان جزئیات"),
        address=models.TextField(blank=True, verbose_name="آدرس"),
        footer_text=models.TextField(blank=True, verbose_name="متن فوتر"),
    )
    logo = models.ImageField(upload_to='site/logo/', blank=True, null=True, verbose_name="لوگو")
    mobile_number = models.CharField(max_length=50, blank=True, verbose_name="شماره موبایل")
    telephone = models.CharField(max_length=50, blank=True, verbose_name="شماره تلفن")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    instagram = models.URLField(blank=True, verbose_name="اینستاگرام")
    linkedin = models.URLField(blank=True, verbose_name="لینکدین")
    whatsapp = models.URLField(blank=True, verbose_name="واتس اپ")
    facebook = models.URLField(blank=True, verbose_name="فیس بوک")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروز رسانی")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "جزئیات سایت"
        verbose_name_plural = "جزئیات سایت"

    def __str__(self):
        return self.safe_translation_getter('site_title', any_language=True) or "عنوان جزئیات"


class SettingLinks(models.Model):
    links = models.ForeignKey(
        Setting,
        on_delete=models.CASCADE,
        related_name="links"
    )
    title = models.CharField('عنوان پیوند', max_length=100, blank=True)
    link_address = models.URLField('آدرس پیوند', blank=True)

    class Meta:
        verbose_name = "پیوند"
        verbose_name_plural = "پیوند"

    def __str__(self):
        return f"آدرس {self.links}"


class AboutUsInfo(TranslatableModel):
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
        banner_title=models.CharField(max_length=200, verbose_name="عنوان بنر صفحه"),
        banner_description=models.TextField(verbose_name="توضیحات بنر صفحه"),
        title=models.CharField("عنوان", max_length=200, blank=True),
        content=models.TextField("محتوا", blank=True,),
        meta_title=models.CharField("متا تایتل", default='Petro Sanat Taraz'),
        meta_description=models.TextField(' متا دسکریپشن', default='توضیحات سایت'),
        og_title=models.CharField('عنوان OG', max_length=255, blank=True, null=True),
        og_description=models.TextField('توضیحات OG', blank=True, null=True),
        og_image=models.ImageField('عکس OG', upload_to="og_images/", blank=True, null=True)
    )
    video = models.FileField('ویدئو',upload_to='videos/', blank=True)
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = " صفحه درباه ما"
        verbose_name_plural = " صفحه درباره ما"

    def __str__(self):
        return self.safe_translation_getter('banner_title', any_language=True) or "about us title"


class AboutUsPost(TranslatableModel):
    translations = TranslatedFields(
        post_title=models.CharField(max_length=200, verbose_name="عنوان پست"),
        post_content=models.TextField(verbose_name="محتوا پست"),
    )
    image = models.ImageField("تصویر پست", upload_to="news/", null=True, blank=True)
    slug = models.SlugField("اسلاگ", unique=True)
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = " پست درباه ما"
        verbose_name_plural = " پست های درباره ما"

    def __str__(self):
        return self.safe_translation_getter('post_title', any_language=True) or "پست درباره ما"


class ContactUsInfo(TranslatableModel):
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
        page_title_one=models.CharField(max_length=200, verbose_name="عنوان صفحه"),
        description_one=models.TextField(blank=True, verbose_name="توضیحات صفحه"),
        page_title_two=models.CharField(max_length=200, blank=True, verbose_name="عنوان"),
        description_two=models.TextField(blank=True, verbose_name="توضیحات"),
        address=models.TextField(blank=True, verbose_name="آدرس"),
        phone=models.CharField(max_length=50, blank=True, verbose_name="تلفن 1"),
        phone_two=models.CharField(max_length=50, blank=True, verbose_name="تلفن 2"),
        phone_three=models.CharField(max_length=50, blank=True, verbose_name="تلفن 3"),
        phone_four=models.CharField(max_length=50, blank=True, verbose_name="تلفن 4"),
        post_code=models.CharField(max_length=50, blank=True, verbose_name="کد پستی"),
        fax=models.CharField(max_length=50, blank=True, verbose_name="فکس"),
    )
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروز رسانی")
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "صفحه تماس با ما"
        verbose_name_plural = "صفحه تماس با ما"

    def __str__(self):
        return self.safe_translation_getter('page_title_one', any_language=True) or "contact us"


class ContactMessage(models.Model):
    full_name = models.CharField("نام کامل", max_length=100)
    email = models.EmailField("ایمیل")
    phone_number = models.CharField("شماره تماس", blank=True, null=True, max_length=15)
    subject = models.CharField("موضوع", max_length=150)
    message = models.TextField("پیام")
    created_at = jmodels.jDateTimeField("تاریخ ارسال", auto_now_add=True)

    is_read = models.BooleanField(default=False, verbose_name="خوانده شده؟")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام ارتباطی"
        verbose_name_plural = "پیام‌های ارتباطی"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class HomeInfo(TranslatableModel):
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
        content=models.TextField("محتوا", blank=True, ),
    )
    image = models.ImageField("تصویر بنر", upload_to="home/", null=True, blank=True)
    video = models.FileField('ویدئو',upload_to='videos/', blank=True)
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)
    canonical_url = models.URLField(
        "آدرس Canonical", blank=True, null=True,
        help_text="اگر خالی باشد، به صورت پیش‌فرض همان آدرس صفحه استفاده می‌شود."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = " صفحه اصلی"
        verbose_name_plural = " صفحه اصلی"

    def __str__(self):
        return self.safe_translation_getter('banner_title', any_language=True)


class FanFact(TranslatableModel):
    translations = TranslatedFields(
        card_title=models.CharField(max_length=100, verbose_name="عنوان کارت"),
        card_content=models.TextField(max_length=500, verbose_name="محتوا کارت"),
    )
    is_active = models.BooleanField("فعال باشد؟", default=False)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروز رسانی", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "کارت"
        verbose_name_plural = "کارت ها"

    def __str__(self):
        return self.safe_translation_getter('card_title', any_language=True)
