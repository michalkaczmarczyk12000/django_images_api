from django.dispatch import receiver
from tiers_config import DEFAULT_CONFIG
from django.db.models.signals import post_migrate, post_save
from . models import UserCustom, Tier
from api.models import ThumbnailSize


@receiver(post_migrate)
def create_default_users_tiers(sender, **kwargs):
    if sender.name == UserCustom._meta.app_label:
        if Tier.objects.filter(name="basic").exists():
            pass
        else:
            basic_tier = Tier.objects.create(
                name="basic",
                get_original_file=DEFAULT_CONFIG['basic']['get_original_file'],
                can_generate_expiring_links=DEFAULT_CONFIG
                ['basic']['can_generate_expiring_links'],
            )
            basic_thumbnail = ThumbnailSize.objects.create(
                **DEFAULT_CONFIG['basic']['thumbnail_size'])
            basic_tier.thumbnail_sizes.set([basic_thumbnail])
        if Tier.objects.filter(name="premium").exists():
            pass
        else:
            premium_tier = Tier.objects.create(
                name="premium",
                get_original_file=DEFAULT_CONFIG
                ['premium']['get_original_file'],
                can_generate_expiring_links=DEFAULT_CONFIG
                ['premium']['can_generate_expiring_links'],
            )
            premium_thumbnail = ThumbnailSize.objects.create(
                **DEFAULT_CONFIG['premium']['thumbnail_size'])
            premium_tier.thumbnail_sizes.set(
                [basic_thumbnail, premium_thumbnail])
        if Tier.objects.filter(name="enterprise").exists():
            pass
        else:
            enterprise_tier = Tier.objects.create(
                name="enterprise",
                get_original_file=DEFAULT_CONFIG
                ['enterprise']['get_original_file'],
                can_generate_expiring_links=DEFAULT_CONFIG
                ['enterprise']['can_generate_expiring_links'],
            )
            enterprise_tier.thumbnail_sizes.set(
                [basic_thumbnail, premium_thumbnail])


@receiver(post_save, sender=UserCustom)
def create_user_account(sender, instance, created, **kwargs):
    if created and not instance.user_tier:
        instance.user_tier = Tier.objects.get(name='basic')
        instance.save()
