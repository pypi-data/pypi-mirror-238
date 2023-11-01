from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.relations.docs.v1.hierarchy import (
    HierarchyV1Doc,
)
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class HierarchyDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**HierarchyDoc.modelviewset_list()),
            "retrieve": extend_schema(**HierarchyDoc.modelviewset_get()),
            "destroy": extend_schema(**HierarchyDoc.modelviewset_delete()),
            "partial_update": extend_schema(**HierarchyDoc.modelviewset_patch()),
            "create": extend_schema(**HierarchyDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Hierarchy - Patch",
            "description": "Hierarchy Patch",
            "tags": ["MODELS : RELATIONS : HIERARCHY"],
            "responses": {
                200: HierarchyModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HierarchyV1Doc.modelviewset_patch_path_examples(),
            "examples": HierarchyV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Hierarchy - List",
            "description": "Hierarchy - All",
            "tags": ["MODELS : RELATIONS : HIERARCHY"],
            "responses": {
                200: HierarchyModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HierarchyV1Doc.modelviewset_list_path_examples(),
            "examples": HierarchyV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Hierarchy - Get",
            "description": "Hierarchy Detail",
            "tags": ["MODELS : RELATIONS : HIERARCHY"],
            "responses": {
                200: HierarchyModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HierarchyV1Doc.modelviewset_get_path_examples(),
            "examples": HierarchyV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Hierarchy - Create",
            "description": "Hierarchy - Create",
            "tags": ["MODELS : RELATIONS : HIERARCHY"],
            "responses": {
                200: HierarchyModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": HierarchyV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Hierarchy - Delete",
            "description": "Hierarchy Delete",
            "tags": ["MODELS : RELATIONS : HIERARCHY"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": HierarchyV1Doc.modelviewset_delete_path_examples(),
        }
