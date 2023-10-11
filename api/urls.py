from django.urls import path
from . import views


urlpatterns = [
    path("", views.ImageListView.as_view(), name="image-list"),
    path("upload/", views.ImageCreateView.as_view(), name="image-create"),
    path("expiring-links/", views.ExpiringLinkListCreateView.as_view(), name='expiring-link-create-list'),
    path("expiring-links/<str:signed_link>/", views.ExpiringLinkDetailView.as_view(), name='expiring-link-detail'),
]
