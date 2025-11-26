from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
