from urllib.parse import unquote


def normalize_farsi_url(path):
    """نرمال‌سازی URL فارسی"""
    decoded = unquote(path)
    # حذف اسلش‌های اضافی
    normalized = '/' + decoded.strip('/')
    return normalized
