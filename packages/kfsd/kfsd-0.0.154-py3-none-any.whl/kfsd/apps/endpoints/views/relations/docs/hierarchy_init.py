from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.relations.docs.v1.hierarchy_init import (
    HierarchyInitV1Doc,
)
from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    HierarchyInitModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class HierarchyInitDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**HierarchyInitDoc.modelviewset_list()),
            "retrieve": extend_schema(**HierarchyInitDoc.modelviewset_get()),
            "destroy": extend_schema(**HierarchyInitDoc.modelviewset_delete()),
            "partial_update": extend_schema(**HierarchyInitDoc.modelviewset_patch()),
            "create": extend_schema(**HierarchyInitDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "HierarchyInit - Patch",
            "description": "HierarchyInit Patch",
            "tags": ["MODELS : RELATIONS : HIERARCHY INIT"],
            "responses": {
                200: HierarchyInitModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HierarchyInitV1Doc.modelviewset_patch_path_examples(),
            "examples": HierarchyInitV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "HierarchyInit - List",
            "description": "HierarchyInit - All",
            "tags": ["MODELS : RELATIONS : HIERARCHY INIT"],
            "responses": {
                200: HierarchyInitModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HierarchyInitV1Doc.modelviewset_list_path_examples(),
            "examples": HierarchyInitV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "HierarchyInit - Get",
            "description": "HierarchyInit Detail",
            "tags": ["MODELS : RELATIONS : HIERARCHY INIT"],
            "responses": {
                200: HierarchyInitModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HierarchyInitV1Doc.modelviewset_get_path_examples(),
            "examples": HierarchyInitV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "HierarchyInit - Create",
            "description": "HierarchyInit - Create",
            "tags": ["MODELS : RELATIONS : HIERARCHY INIT"],
            "responses": {
                200: HierarchyInitModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": HierarchyInitV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "HierarchyInit - Delete",
            "description": "HierarchyInit Delete",
            "tags": ["MODELS : RELATIONS : HIERARCHY INIT"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": HierarchyInitV1Doc.modelviewset_delete_path_examples(),
        }
