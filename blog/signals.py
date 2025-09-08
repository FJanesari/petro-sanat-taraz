from django_ckeditor_5.fields import CKEditor5Field as BaseCKEditor5Field
import bleach
from html import unescape


class CleanedCKEditor5Field(BaseCKEditor5Field):
    def clean(self, value, instance):
        value = super().clean(value, instance)
        if value:
            # تبدیل entities به کاراکترهای واقعی (مثل &lt; به <)
            decoded_content = unescape(value)

            # پاکسازی محتوا
            cleaned_content = self._sanitize_html(decoded_content)

            # بررسی نهایی برای کدهای مخرب
            if self._contains_malicious_code(cleaned_content):
                raise ValueError("محتویات خطرناک شناسایی شد!")

            return cleaned_content
        return value

    def _sanitize_html(self, content):
        """پاکسازی کامل HTML"""
        allowed_tags = [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'em', 'ul', 'ol', 'li', 'a',
            'img', 'table', 'tr', 'td', 'th', 'br',
            'div', 'span', 'blockquote', 'hr'
        ]

        allowed_attributes = {
            'a': ['href', 'title', 'target', 'rel'],
            'img': ['src', 'alt', 'width', 'height'],
            '*': ['class', 'style']
        }

        return bleach.clean(
            content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True,
            strip_comments=True
        )

    def _contains_malicious_code(self, content):
        """بررسی وجود کدهای مخرب"""
        forbidden_patterns = [
            'script', 'javascript:', 'onload=', 'onerror=',
            'onclick=', 'onmouseover=', 'iframe', 'object',
            'embed', 'eval(', 'document.', 'window.'
        ]
        return any(pattern.lower() in content.lower() for pattern in forbidden_patterns)
