from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.relations.docs.v1.hrel import (
    HRelV1Doc,
    HrelHierarchyDocV1,
)
from kfsd.apps.endpoints.serializers.relations.hrel import (
    HRelViewModelSerializer,
)
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
    SuccessSerializer,
)


class HRelHierarchyDoc:
    @staticmethod
    def modelviewset():
        return {
            "post": extend_schema(**HRelHierarchyDoc.modelviewset_post()),
            "delete": extend_schema(**HRelHierarchyDoc.modelviewset_delete()),
        }

    def modelviewset_post():
        return {
            "summary": "Hierarchy - Add",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: SuccessSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "parameters": HrelHierarchyDocV1.modelviewset_parameters(),
        }

    def modelviewset_delete():
        return {
            "summary": "Hierarchy - Delete",
            "description": "Hierarchy - Delete",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: SuccessSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "parameters": HrelHierarchyDocV1.modelviewset_parameters(),
        }


class HRelDoc:
    @staticmethod
    def add_child_view():
        return {
            "summary": "Hierarchy - Add",
            "description": "Hierarchy - Add",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: SuccessSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HRelV1Doc.heierarchy_view_path_examples(),
            "examples": HRelV1Doc.heierarchy_view_examples(),
        }

    @staticmethod
    def del_child_view():
        return {
            "summary": "Hierarchy - Del",
            "description": "Hierarchy - Del",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: SuccessSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HRelV1Doc.heierarchy_view_path_examples(),
            "examples": HRelV1Doc.heierarchy_view_examples(),
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**HRelDoc.modelviewset_list()),
            "retrieve": extend_schema(**HRelDoc.modelviewset_get()),
            "destroy": extend_schema(**HRelDoc.modelviewset_delete()),
            "partial_update": extend_schema(**HRelDoc.modelviewset_patch()),
            "create": extend_schema(**HRelDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "HRel - Patch",
            "description": "HRel Patch",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: HRelViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HRelV1Doc.modelviewset_patch_path_examples(),
            "examples": HRelV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "HRel - List",
            "description": "HRel - All",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: HRelViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HRelV1Doc.modelviewset_list_path_examples(),
            "examples": HRelV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "HRel - Get",
            "description": "HRel Detail",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: HRelViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": HRelV1Doc.modelviewset_get_path_examples(),
            "examples": HRelV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "HRel - Create",
            "description": "HRel - Create",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {
                200: HRelViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": HRelV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "HRel - Delete",
            "description": "HRel Delete",
            "tags": ["MODELS : RELATIONS : HREL"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": HRelV1Doc.modelviewset_delete_path_examples(),
        }
