from drf_spectacular.utils import extend_schema, OpenApiTypes

from kfsd.apps.endpoints.views.validations.docs.v1.rule import RuleV1Doc
from kfsd.apps.endpoints.serializers.validations.rule import RuleViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class RuleDoc:
    @staticmethod
    def exec_view():
        return {
            "summary": "Rule - Exec",
            "description": "Rule Exec",
            "tags": ["MODELS : VALIDATIONS : RULE"],
            "responses": {
                200: OpenApiTypes.ANY,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RuleV1Doc.exec_view_path_examples(),
            "examples": RuleV1Doc.exec_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**RuleDoc.modelviewset_list()),
            "retrieve": extend_schema(**RuleDoc.modelviewset_get()),
            "destroy": extend_schema(**RuleDoc.modelviewset_delete()),
            "partial_update": extend_schema(**RuleDoc.modelviewset_patch()),
            "create": extend_schema(**RuleDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Rule - Patch",
            "description": "Rule Patch",
            "tags": ["MODELS : VALIDATIONS : RULE"],
            "responses": {
                200: RuleViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RuleV1Doc.modelviewset_patch_path_examples(),
            "examples": RuleV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Rule - List",
            "description": "Rule - All",
            "tags": ["MODELS : VALIDATIONS : RULE"],
            "responses": {
                200: RuleViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RuleV1Doc.modelviewset_list_path_examples(),
            "examples": RuleV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Rule - Get",
            "description": "Rule Detail",
            "tags": ["MODELS : VALIDATIONS : RULE"],
            "responses": {
                200: RuleViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RuleV1Doc.modelviewset_get_path_examples(),
            "examples": RuleV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Rule - Create",
            "description": "Rule - Create",
            "tags": ["MODELS : VALIDATIONS : RULE"],
            "responses": {
                200: RuleViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": RuleV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Rule - Delete",
            "description": "Rule Delete",
            "tags": ["MODELS : VALIDATIONS : RULE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": RuleV1Doc.modelviewset_delete_path_examples(),
        }
