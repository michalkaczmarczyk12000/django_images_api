from django.shortcuts import render
from rest_framework.decorators import api_view
from  .models import Image

# Create your views here.


@api_view(['POST'])
def home(request, *args, **kwargs):
    return render(request)
