from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.validations.rule import Rule, RULE_MAX_LENGTH
from kfsd.apps.models.tables.validations.policy import Policy
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.endpoints.serializers.base import get_serializer_val


class PrefetchItemSerializer(serializers.Serializer):
    expr = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    var = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(MAX_LENGTH),
        ],
    )


class ExprSerializer(serializers.Serializer):
    expr = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(RULE_MAX_LENGTH),
        ],
    )


class RuleSerializer(serializers.Serializer):
    expr = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(RULE_MAX_LENGTH),
        ],
    )
    anyOf = serializers.ListSerializer(
        child=ExprSerializer(),
        required=False,
    )
    allOf = serializers.ListSerializer(
        child=ExprSerializer(),
        required=False,
    )


class RuleModelSerializer(BaseModelSerializer):
    policy = serializers.SlugRelatedField(
        required=True,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Policy.objects.all(),
    )
    prefetch = serializers.ListSerializer(
        child=PrefetchItemSerializer(), required=False, allow_empty=True
    )
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    values = serializers.JSONField()

    expr = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(RULE_MAX_LENGTH),
        ],
    )
    anyOf = serializers.ListSerializer(
        child=RuleSerializer(), required=False, allow_empty=True
    )
    allOf = serializers.ListSerializer(
        child=RuleSerializer(), required=False, allow_empty=True
    )

    def validate(self, data):
        count = 0
        for field in ["expr", "anyOf", "allOf"]:
            fieldVal = get_serializer_val(self, data, field)
            if fieldVal:
                count += 1

        if count == 0:
            raise serializers.ValidationError(
                "Atleast one value needs to be set among expr, anyOf and allOf"
            )

        if count > 1:
            raise serializers.ValidationError(
                "Only one value can be set among expr, anyOf and allOf"
            )

        return data

    class Meta:
        model = Rule
        fields = "__all__"


class RuleViewModelSerializer(RuleModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Rule
        exclude = ("created", "updated", "id")
