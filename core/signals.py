from django_ckeditor_5.fields import CKEditor5Field as BaseCKEditor5Field
import bleach
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES
from html import unescape, escape
import re


class CleanedCKEditor5Field(BaseCKEditor5Field):
    """
    پاکسازی محتوی CKEditor5:
      - فیلتر ایمنِ declarationهای CSS (width, height, max-width, aspect-ratio, float, text-align)
      - پیش‌ذخیرهٔ style و src در attribute‌های موقت تا bleach آنها را حذف نکند
      - بازگرداندن attributeهای موقت به style/src بعد از bleach
    """

    _ALLOWED_STYLE_PROPS = {
        "width", "height", "float", "text-align", "max-width", "aspect-ratio"
    }

    def clean(self, value, instance):
        value = super().clean(value, instance)
        if value:
            decoded = unescape(value)
            cleaned = self._sanitize_html(decoded)

            if self._contains_malicious_code(cleaned):
                raise ValueError("محتویات خطرناک شناسایی شد!")

            return cleaned
        return value

    def _sanitize_html(self, content: str) -> str:
        # regex برای گرفتن style="..." و src="..."
        style_re = re.compile(
            r'\sstyle\s*=\s*(?P<quote>["\'])(?P<val>.*?)(?P=quote)',
            flags=re.IGNORECASE | re.DOTALL
        )
        src_re = re.compile(
            r'\ssrc\s*=\s*(?P<quote>["\'])(?P<val>.*?)(?P=quote)',
            flags=re.IGNORECASE | re.DOTALL
        )

        def _is_safe_css_value(prop: str, val: str) -> bool:
            v = val.strip().lower()

            if v in ("auto", "inherit", "initial", "unset"):
                return True

            if prop == "text-align":
                return v in ("left", "right", "center", "justify")

            if prop == "float":
                return v in ("left", "right", "none")

            if prop in ("width", "height", "max-width"):
                # قبول اعشار + واحد یا بدون واحد: مثال 49.41%, 100px, 3.5em, 12
                return re.match(r'^[0-9]+(\.[0-9]+)?(px|em|rem|%)?$', v) is not None

            if prop == "aspect-ratio":
                # مثال: 1024/688
                return re.match(r'^[0-9]+/[0-9]+$', v) is not None

            return False

        def _clean_style_attr(style_value: str) -> str:
            kept = []
            for decl in style_value.split(";"):
                if not decl.strip() or ":" not in decl:
                    continue
                prop, val = decl.split(":", 1)
                prop = prop.strip().lower()
                val = val.strip()
                if prop in self._ALLOWED_STYLE_PROPS and _is_safe_css_value(prop, val):
                    kept.append(f"{prop}: {val}")
            return "; ".join(kept)

        # --- 1) تبدیل style="..." -> data-cke-clean-style="..." (فقط اگر declaration مجاز داشته باشد)
        def _style_preparer(m: re.Match) -> str:
            raw = m.group("val")
            cleaned = _clean_style_attr(raw)
            if not cleaned:
                return ""  # حذف کامل اگر چیزی برای نگه داشتن نیست
            return f' data-cke-clean-style="{escape(cleaned, quote=True)}"'

        prepared = style_re.sub(_style_preparer, content)

        # --- 2) تبدیل src="..." -> data-cke-clean-src="..."
        # اینجا همه‌ی srcها را تبدیل می‌کنیم; در پایان دوباره به src بازمی‌گردد.
        def _src_preparer(m: re.Match) -> str:
            raw = m.group("val")
            # escape برای ایمنی داخل attribute
            return f' data-cke-clean-src="{escape(raw, quote=True)}"'

        prepared = src_re.sub(_src_preparer, prepared)

        # --- 3) آماده‌سازی تگ‌ها و attributeها برای bleach
        allowed_tags = list(ALLOWED_TAGS) + [
            "p", "h1", "h2", "h3", "h4", "h5", "h6",
            "img", "table", "thead", "tbody", "tr", "td", "th",
            "div", "span", "blockquote", "hr", "br", "pre", "code",
            "ul", "ol", "li", "figure"
        ]

        # سازگارسازی ALLOWED_ATTRIBUTES به یک دیکشنری که مقادیرش لیست‌اند
        base_attrs = {}
        for k, v in ALLOWED_ATTRIBUTES.items():
            if isinstance(v, (list, tuple, set)):
                base_attrs[k] = list(v)
            elif isinstance(v, str):
                base_attrs[k] = [v]
            else:
                try:
                    base_attrs[k] = list(v)
                except Exception:
                    base_attrs[k] = []

        # به‌صورت صریح اجازهٔ attributeهای ضروری برای img و سایر تگ‌ها را اضافه می‌کنیم
        img_attrs = ["src", "srcset", "alt", "width", "height", "loading", "decoding", "class", "data-cke-clean-style", "data-cke-clean-src"]
        for a in img_attrs:
            if a not in base_attrs.setdefault("img", []):
                base_attrs["img"].append(a)

        # برای figure/div/span و کلیه تگ‌ها attribute موقت و class را اضافه کن
        extra_tags = ["figure", "div", "span", "a"]
        for t in extra_tags:
            lst = base_attrs.setdefault(t, [])
            if "class" not in lst:
                lst.append("class")
            if "data-cke-clean-style" not in lst:
                lst.append("data-cke-clean-style")
            if "data-cke-clean-src" not in lst:
                lst.append("data-cke-clean-src")

        # به همه تگ‌ها اجازهٔ class و attribute موقت بده (فقط اگر قبلاً نبوده)
        all_list = base_attrs.setdefault("*", [])
        if "class" not in all_list:
            all_list.append("class")
        if "data-cke-clean-style" not in all_list:
            all_list.append("data-cke-clean-style")
        if "data-cke-clean-src" not in all_list:
            all_list.append("data-cke-clean-src")

        # --- 4) فراخوانی bleach.clean
        # سعی می‌کنیم پارامترهای مربوط به پروتکل‌ها را هم بفرستیم (برای نسخه‌های مختلف bleach سازگار)
        bleach_kwargs = dict(
            tags=allowed_tags,
            attributes=base_attrs,
            strip=True,
            strip_comments=True,
        )
        # اجازهٔ URLهای معمول و آدرس‌های data و relative ("" یا None) را اضافه می‌کنیم
        # برخی نسخه‌ها 'protocols' می‌خواهند و برخی 'allowed_protocols'
        try:
            bleach_kwargs["protocols"] = ["http", "https", "data", "mailto", ""]
        except Exception:
            pass

        try:
            sanitized = bleach.clean(prepared, **bleach_kwargs)
        except TypeError:
            # اگر bleach.clean پارامتر 'protocols' را قبول نکرد، تلاش می‌کنیم با 'allowed_protocols'
            bleach_kwargs.pop("protocols", None)
            try:
                bleach_kwargs["allowed_protocols"] = {"http", "https", "data", "mailto", ""}
                sanitized = bleach.clean(prepared, **bleach_kwargs)
            except Exception:
                # در بدترین حالت بدون پارامتر پروتکل فراخوانی کن
                sanitized = bleach.clean(prepared, tags=allowed_tags, attributes=base_attrs, strip=True, strip_comments=True)

        # --- 5) بازیابی attributeهای موقت به style و src
        post_style_re = re.compile(
            r'\sdata-cke-clean-style\s*=\s*(?P<quote>["\'])(?P<val>.*?)(?P=quote)',
            flags=re.IGNORECASE | re.DOTALL
        )
        def _post_style_replacer(m: re.Match) -> str:
            val = unescape(m.group("val"))
            return f' style="{val}"'
        restored = post_style_re.sub(_post_style_replacer, sanitized)

        post_src_re = re.compile(
            r'\sdata-cke-clean-src\s*=\s*(?P<quote>["\'])(?P<val>.*?)(?P=quote)',
            flags=re.IGNORECASE | re.DOTALL
        )
        def _post_src_replacer(m: re.Match) -> str:
            val = unescape(m.group("val"))
            return f' src="{val}"'
        final = post_src_re.sub(_post_src_replacer, restored)

        return final

    def _contains_malicious_code(self, content: str) -> bool:
        forbidden_patterns = [
            "script", "javascript:", "onload=", "onerror=",
            "onclick=", "onmouseover=", "iframe", "object",
            "embed", "eval(", "document.", "window."
        ]
        low = content.lower()
        return any(patt in low for patt in forbidden_patterns)
