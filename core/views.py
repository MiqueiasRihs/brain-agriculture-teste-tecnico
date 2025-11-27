import logging

from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from core.serializers import SignupSerializer
from producers.serializers import ProducerSerializer


class BaseViewSet(viewsets.ModelViewSet):
    logger = logging.getLogger("brain_agriculture.api")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAuthenticated]
    owner_lookup_field = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return queryset.none()

        if user.is_staff:
            return queryset

        if not self.owner_lookup_field:
            return queryset

        return queryset.filter(**{self.owner_lookup_field: user})

    def _get_resource_label(self):
        queryset = getattr(self, "queryset", None)
        if queryset is not None:
            model = getattr(queryset, "model", None)
            if model is not None:
                return model.__name__

        serializer_class = getattr(self, "serializer_class", None)
        if serializer_class is not None:
            meta = getattr(serializer_class, "Meta", None)
            model = getattr(meta, "model", None)
            if model is not None:
                return model.__name__

        return self.__class__.__name__

    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        self.logger.info(
            "%s created (id=%s) by user=%s",
            self._get_resource_label(),
            getattr(instance, "pk", None),
            getattr(self.request.user, "pk", None),
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        self.logger.info(
            "%s updated (id=%s) by user=%s",
            self._get_resource_label(),
            getattr(instance, "pk", None),
            getattr(self.request.user, "pk", None),
        )

    def perform_destroy(self, instance):
        resource_id = getattr(instance, "pk", None)
        resource_label = self._get_resource_label()
        super().perform_destroy(instance)
        self.logger.info(
            "%s deleted (id=%s) by user=%s",
            resource_label,
            resource_id,
            getattr(self.request.user, "pk", None),
        )


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = SignupSerializer
    logger = logging.getLogger("brain_agriculture.auth")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        producer_data = ProducerSerializer(user.producer).data

        self.logger.info("New signup completed for user=%s", user.pk)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                },
                "producer": producer_data,
            },
            status=status.HTTP_201_CREATED,
        )
