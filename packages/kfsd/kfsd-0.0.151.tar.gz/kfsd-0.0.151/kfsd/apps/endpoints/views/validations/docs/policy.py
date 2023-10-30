from drf_spectacular.utils import extend_schema, OpenApiTypes

from kfsd.apps.endpoints.views.validations.docs.v1.policy import PolicyV1Doc
from kfsd.apps.endpoints.serializers.validations.policy import PolicyViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class PolicyDoc:
    @staticmethod
    def exec_view():
        return {
            "summary": "Policy - Exec",
            "description": "Policy Exec",
            "tags": ["MODELS : VALIDATIONS : POLICY"],
            "responses": {
                200: OpenApiTypes.ANY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PolicyV1Doc.exec_view_path_examples(),
            "examples": PolicyV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**PolicyDoc.modelviewset_list()),
            "retrieve": extend_schema(**PolicyDoc.modelviewset_get()),
            "destroy": extend_schema(**PolicyDoc.modelviewset_delete()),
            "partial_update": extend_schema(**PolicyDoc.modelviewset_patch()),
            "create": extend_schema(**PolicyDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Policy - Patch",
            "description": "Policy Patch",
            "tags": ["MODELS : VALIDATIONS : POLICY"],
            "responses": {
                200: PolicyViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PolicyV1Doc.modelviewset_patch_path_examples(),
            "examples": PolicyV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Policy - List",
            "description": "Policy - All",
            "tags": ["MODELS : VALIDATIONS : POLICY"],
            "responses": {
                200: PolicyViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PolicyV1Doc.modelviewset_list_path_examples(),
            "examples": PolicyV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Policy - Get",
            "description": "Policy Detail",
            "tags": ["MODELS : VALIDATIONS : POLICY"],
            "responses": {
                200: PolicyViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PolicyV1Doc.modelviewset_get_path_examples(),
            "examples": PolicyV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Policy - Create",
            "description": "Policy - Create",
            "tags": ["MODELS : VALIDATIONS : POLICY"],
            "responses": {
                200: PolicyViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": PolicyV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Policy - Delete",
            "description": "Policy Delete",
            "tags": ["MODELS : VALIDATIONS : POLICY"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": PolicyV1Doc.modelviewset_delete_path_examples(),
        }
