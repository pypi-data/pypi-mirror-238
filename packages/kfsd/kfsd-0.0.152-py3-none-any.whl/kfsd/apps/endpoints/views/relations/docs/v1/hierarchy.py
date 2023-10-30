from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class HierarchyV1Doc:
    @staticmethod
    def modelviewset_list_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.QUERY,
                name="page",
                required=False,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample("Example 1", summary="Pagination", value=1),
                    OpenApiExample("Example 2", summary="Pagination", value=2),
                ],
            )
        ]

    @staticmethod
    def modelviewset_list_examples():
        return [
            OpenApiExample(
                "Hierarchy - List All",
                value=[
                    {
                        "identifier": "EXCHANGE=kubefacets.exchange",
                        "name": "kubefacets.exchange",
                        "attrs": {"durable": True, "exchange_type": "direct"},
                    }
                ],
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_get_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Hierarchy - Get",
                        summary="Hierarchy Identifier",
                        description="Hierarchy - Get",
                        value="EXCHANGE=kubefacets.exchange",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Hierarchy - Get",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange",
                    "name": "kubefacets.exchange",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Hierarchy - Create",
                value={
                    "name": "kubefacets.exchange",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Hierarchy - Create",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange",
                    "name": "kubefacets.exchange",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_delete_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Hierarchy - Delete",
                        summary="Hierarchy Identifier",
                        description="Hierarchy - Delete",
                        value="EXCHANGE=kubefacets.exchange",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Hierarchy - Patch",
                        summary="Hierarchy Identifier",
                        description="Hierarchy - Patch",
                        value="EXCHANGE=kubefacets.exchange",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Hierarchy - Patch",
                value={
                    "name": "kubefacets.exchange.v1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Hierarchy - Patch",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange.v1",
                    "name": "kubefacets.exchange.v1",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=False,
                response_only=True,
            ),
        ]
