from django.http import HttpResponsePermanentRedirect
from django.core.cache import cache
from .models import Redirect
import logging
from urllib.parse import unquote, urlparse

logger = logging.getLogger(__name__)


class RedirectMiddleware:
    """Middleware for dynamic SEO redirects (DB-based, cache-aware, encoding-safe)."""

    CACHE_KEY = "redirects_cache"
    CACHE_TIMEOUT = 3600  # 1 hour

    def __init__(self, get_response):
        self.get_response = get_response
        self._refresh_cache()

    # -----------------------------
    # Utils
    # -----------------------------
    def _normalize_path(self, path: str) -> str:
        """Normalize URLs (decode + strip + ensure leading slash)."""
        try:
            # استخراج فقط بخش path اگر URL کامل (با دامنه) داده شده باشد
            parsed = urlparse(path)
            if parsed.path:
                path = parsed.path

            # دیکد و نرمال‌سازی
            decoded_path = unquote(path)
            normalized = decoded_path.strip().rstrip("/")

            if not normalized.startswith("/"):
                normalized = "/" + normalized

            return normalized
        except Exception as e:
            logger.warning(f"[RedirectMiddleware] Path normalization failed for {path}: {e}")
            return path

    def _get_redirects_dict(self):
        """Load active redirects from DB into cache."""
        try:
            redirects = Redirect.objects.filter(active=True)
            redirects_dict = {}

            for r in redirects:
                old_path = self._normalize_path(r.old_path)
                new_path = self._normalize_path(r.new_path)

                redirects_dict[old_path] = new_path

                if not old_path.endswith("/"):
                    redirects_dict[old_path + "/"] = new_path

            logger.info(f"[RedirectMiddleware] Loaded {len(redirects_dict)} redirects into cache")
            return redirects_dict

        except Exception as e:
            logger.error(f"[RedirectMiddleware] Failed to load redirects: {e}")
            return {}

    def _refresh_cache(self):
        """Refresh redirect cache."""
        redirects_dict = self._get_redirects_dict()
        cache.set(self.CACHE_KEY, redirects_dict, self.CACHE_TIMEOUT)
        logger.info(f"[RedirectMiddleware] Cache refreshed with {len(redirects_dict)} items")

    # -----------------------------
    # Matching logic
    # -----------------------------
    def _find_redirect_match(self, path: str, redirects_cache: dict):
        """Find redirect target with normalization and encoding handling."""
        normalized_path = self._normalize_path(path)
        candidates = {
            path,
            unquote(path),
            normalized_path,
        }

        for test_path in candidates:
            if test_path in redirects_cache:
                return redirects_cache[test_path]
            # check both with and without trailing slash
            if not test_path.endswith("/") and test_path + "/" in redirects_cache:
                return redirects_cache[test_path + "/"]
            if test_path.endswith("/") and test_path[:-1] in redirects_cache:
                return redirects_cache[test_path[:-1]]
        return None

    # -----------------------------
    # Main call
    # -----------------------------
    def __call__(self, request):
        path = request.path_info

        if path.startswith(("/static/", "/media/", "/admin/")):
            return self.get_response(request)

        redirects_cache = cache.get(self.CACHE_KEY)
        if not redirects_cache:
            self._refresh_cache()
            redirects_cache = cache.get(self.CACHE_KEY, {})

        new_path = self._find_redirect_match(path, redirects_cache)

        if new_path:
            if not new_path.startswith(("http://", "https://", "/")):
                new_path = "/" + new_path

            logger.info(f"[RedirectMiddleware] Redirect match: {path} → {new_path}")
            return HttpResponsePermanentRedirect(new_path)

        return self.get_response(request)

    @classmethod
    def refresh_redirects_cache(cls):
        """Manual trigger for cache refresh (via signals)."""
        instance = cls(lambda x: x)
        instance._refresh_cache()
