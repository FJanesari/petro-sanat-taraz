from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Redirect
from .middleware import RedirectMiddleware
import logging

logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], sender=Redirect)
def refresh_redirects_cache(sender, **kwargs):
    """بروزرسانی کش هنگام تغییرات در مدل Redirect"""
    try:
        RedirectMiddleware.refresh_redirects_cache()
        logger.info("Redirects cache updated after model change")
    except Exception as e:
        logger.error(f"Failed to update redirects cache: {e}")


# سیگنال برای زمانی که وضعیت active تغییر می‌کنه
@receiver(post_save, sender=Redirect)
def handle_redirect_active_change(sender, instance, **kwargs):
    """اگر وضعیت active تغییر کرد، کش رو بروز کن"""
    try:
        if kwargs.get('update_fields') and 'active' in kwargs.get('update_fields', set()):
            RedirectMiddleware.refresh_redirects_cache()
            logger.info("Redirects cache updated after active status change")
    except Exception as e:
        logger.error(f"Failed to update redirects cache after active change: {e}")
