
from rest_framework import status
from rest_framework.response import Response

from core.views import BaseViewSet
from producers.models import Producer
from producers.serializers import ProducerSerializer

class ProducerViewSet(BaseViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    filterset_fields = ['name', 'document_type', 'document']
    ordering_fields = ['name', 'created_at']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)