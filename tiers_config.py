from django.conf import settings

MIN_EXPIRY_LINK_TIME = getattr(settings, 'MIN_EXPIRY_LINK_TIME', 300)
MAX_EXPIRY_LINK_TIME = getattr(settings, 'MAX_EXPIRY_LINK_TIME', 30000)
DEFAULT_CONFIG = {
    'basic': dict(
        thumbnail_size=dict(width=200, height=200),
        get_original_file=False,
        can_generate_expiring_links=False,
    ),
    'premium': dict(
        thumbnail_size=dict(width=200, height=400),
        get_original_file=True,
        can_generate_expiring_links=False,
    ),
    'enterprise': dict(
        get_original_file=True,
        can_generate_expiring_links=True,
    ),
}
