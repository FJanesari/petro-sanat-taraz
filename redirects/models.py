from django.db import models


class Redirect(models.Model):
    old_path = models.CharField(
        "آدرس قدیمی", max_length=512, unique=True,
    )
    new_path = models.CharField(
        "آدرس جدید", max_length=512,
    )
    active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "ریدایرکت"
        verbose_name_plural = "ریدایرکت ها"

    def __str__(self):
        return f"{self.old_path} → {self.new_path}"
