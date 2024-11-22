from rest_framework import serializers
from constance import config


class ConstanceSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    def to_representation(self, instance):
        return {
            "key": instance[0],
            "value": getattr(config, instance[0]),
        }
