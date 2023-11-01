from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.relations.docs.v1.relation import RelationV1Doc
from kfsd.apps.endpoints.serializers.relations.relation import (
    RelationViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class RelationDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**RelationDoc.modelviewset_list()),
            "retrieve": extend_schema(**RelationDoc.modelviewset_get()),
            "destroy": extend_schema(**RelationDoc.modelviewset_delete()),
            "partial_update": extend_schema(**RelationDoc.modelviewset_patch()),
            "create": extend_schema(**RelationDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Relation - Patch",
            "description": "Relation Patch",
            "tags": ["MODELS : RELATIONS : RELATION"],
            "responses": {
                200: RelationViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RelationV1Doc.modelviewset_patch_path_examples(),
            "examples": RelationV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Relation - List",
            "description": "Relation - All",
            "tags": ["MODELS : RELATIONS : RELATION"],
            "responses": {
                200: RelationViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RelationV1Doc.modelviewset_list_path_examples(),
            "examples": RelationV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Relation - Get",
            "description": "Relation Detail",
            "tags": ["MODELS : RELATIONS : RELATION"],
            "responses": {
                200: RelationViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RelationV1Doc.modelviewset_get_path_examples(),
            "examples": RelationV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Relation - Create",
            "description": "Relation - Create",
            "tags": ["MODELS : RELATIONS : RELATION"],
            "responses": {
                200: RelationViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": RelationV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Relation - Delete",
            "description": "Relation Delete",
            "tags": ["MODELS : RELATIONS : RELATION"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": RelationV1Doc.modelviewset_delete_path_examples(),
        }
