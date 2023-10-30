from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.validations.rule import RuleModelViewSet
from kfsd.apps.endpoints.views.validations.policy import PolicyModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("validations/rule", RuleModelViewSet, basename="rule")
router.register("validations/policy", PolicyModelViewSet, basename="policy")

urlpatterns = [
    path("", include(router.urls)),
]
