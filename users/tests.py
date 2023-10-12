from django.test import TestCase
from django.contrib.auth import get_user_model
from . models import Tier


class CustomUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_enterprise = get_user_model().objects.create(
            username='enterprise@mail.com',
            password="pswd",
        )
        user_tier = Tier.objects.get(name='enterprise')
        cls.user_enterprise.user_tier = user_tier

        cls.user_premium = get_user_model().objects.create(
            username='premium@mail.com',
            password="pswd",
        )
        user_tier = Tier.objects.get(name='premium')
        cls.user_premium.user_tier = user_tier

        cls.user_basic = get_user_model().objects.create(
            username='basic@mail.com',
            password="pswd",
        )
        user_tier = Tier.objects.get(name='basic')
        cls.user_basic.user_tier = user_tier

    def test_users_tier(self):
        self.assertEqual(self.user_basic.user_tier.name, "basic")
        self.assertEqual(self.user_premium.user_tier.name, "premium")
        self.assertEqual(self.user_enterprise.user_tier.name, "enterprise")

    def test_can_get_original_file(self):
        self.assertFalse(self.user_basic.user_tier.get_original_file)
        self.assertTrue(self.user_premium.user_tier.get_original_file)
        self.assertTrue(self.user_enterprise.user_tier.get_original_file)

    def test_can_generate_expiring_links(self):
        self.assertFalse(self.user_basic.user_tier.
                         can_generate_expiring_links)
        self.assertFalse(self.user_premium.
                         user_tier.can_generate_expiring_links)
        self.assertTrue(self.user_enterprise.user_tier.
                        can_generate_expiring_links)
