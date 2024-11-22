from chat_app.api.v1.serializers import ConstanceSerializer

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from constance import config
from constance import settings as constance_settings


class ConstanceViewSet(ViewSet):
    def list(self, request):
        keys = constance_settings.CONFIG.keys()
        constance_values = [(key, getattr(config, key)) for key in keys]
        serializer = ConstanceSerializer(constance_values, many=True)
        return Response(serializer.data)
