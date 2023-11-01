from rest_framework import serializers
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.signals.signal import Signal
from kfsd.apps.models.tables.signals.webhook import Webhook
from kfsd.apps.models.tables.requests.endpoint import Endpoint


class WebhookModelSerializer(BaseModelSerializer):
    signals = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Signal.objects.all(),
    )
    endpoint = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Endpoint.objects.all(),
    )

    class Meta:
        model = Webhook
        fields = "__all__"


class WebhookViewModelSerializer(WebhookModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Webhook
        exclude = ("created", "updated", "id")
