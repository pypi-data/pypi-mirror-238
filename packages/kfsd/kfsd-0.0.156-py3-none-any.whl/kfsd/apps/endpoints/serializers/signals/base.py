from rest_framework import serializers
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer


class BaseSignalModelSerializer(BaseModelSerializer):
    data = serializers.JSONField(default=dict)
    status = serializers.ChoiceField(
        choices=["PENDING", "IN-PROGRESS", "ERROR", "COMPLETED"], default="IN-PROGRESS"
    )
    attempts = serializers.IntegerField(default=0)
    debug_info = serializers.JSONField(default=dict, read_only=True)
