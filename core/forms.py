from django.core.exceptions import ValidationError
from django import forms
from .models import ContactMessage


class SingleActiveInstanceMixin:
    active_field_name = "is_active"
    model_class = None

    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get(self.active_field_name)

        if is_active:
            if self.model_class is None:
                raise ValueError("model_class must be set in the subclass.")
            existing_active = self.model_class.objects.exclude(pk=self.instance.pk).filter(**{
                self.active_field_name: True
            })
            if existing_active.exists():
                raise ValidationError(f"فقط یک {self.model_class._meta.verbose_name} می‌تواند فعال باشد.")

        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "phone_number", "subject", "message"]

