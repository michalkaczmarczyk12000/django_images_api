from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.models import Tier
from .models import Image, ExpiringLink
from PIL import Image as pil_img
from django.urls import reverse
from rest_framework import status

from io import BytesIO
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your tests here.


def create_test_image():
    test_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                   'test_image', 'test.png')

    with open(test_image_path, 'rb') as f:
        image_data = BytesIO(f.read())

    image = pil_img.open(image_data)
    image_file = BytesIO()
    image.save(image_file, format='png')
    image_file.seek(0)

    return InMemoryUploadedFile(
        image_file,
        None,
        'test.png',
        'image/png',
        image_file.tell,
        None
    )


class ImageModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username='user_test',
            email='test@mail.com',
            password='password',
            is_staff=True,
            is_active=True,
        )
        cls.image_file = create_test_image()
        cls.image = Image.objects.create(
            user=cls.user,
            image=cls.image_file,
        )
        cls.expected_image_path = cls.image.get_original_image_url
        cls.expected_image_name = 'test'
        cls.expected_ext = '.png'

    def test_img_owner(self):
        self.assertEqual(self.image.user.username, "user_test")
        self.assertEqual(self.image.user.email, 'test@mail.com')

    def test_get_original_url(self):
        self.assertEqual(self.image.get_original_image_url,
                         self.expected_image_path)


class ImageApiTestCase(APITestCase):
    def setUp(self) -> None:
        enterprise = Tier.objects.get(id=3)
        self.user = get_user_model().objects.create_user(
            username='enetrprise',
            password='password',
            user_tier=enterprise)
        self.client.login(username='enetrprise', password='password')
        self.image_file = create_test_image()

    def test_create_image(self):
        url = reverse('image-create')
        data = {'image': self.image_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_images(self):
        Image.objects.create(user=self.user, image=self.image_file)
        url = reverse('image-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expiring_link_detail(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        url = reverse('expiring-link-create-list')
        data = {'image': image.id, 'expires_in': '3600'}
        response = self.client.post(url, data, format='json')
        link = response.data.get('link').split('/')[-2]
        url = reverse('expiring-link-detail', kwargs={'signed_link': link})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expiring_link_detail_with_expired_link(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        expiring_link = ExpiringLink.objects.create(image=image,
                                                    link='test_link',
                                                    expires_in=-3600)
        url = reverse('expiring-link-detail',
                      kwargs={'signed_link': expiring_link.link})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_expiring_link(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        url = reverse('expiring-link-create-list')
        data = {'image': image.id, 'expires_in': '3600'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_expiring_links(self):
        image = Image.objects.create(user=self.user, image=self.image_file)
        ExpiringLink.objects.create(image=image, link='test_link',
                                    expires_in='3600')
        url = reverse('expiring-link-create-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
