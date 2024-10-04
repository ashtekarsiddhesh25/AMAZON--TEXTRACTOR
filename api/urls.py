from django.urls import path
from .views import TextractAPIView

urlpatterns = [
    path('textract/', TextractAPIView.as_view(), name='textract'),
]
