from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class HrelHierarchyDocV1:
    @staticmethod
    def modelviewset_parameters():
        return [
            OpenApiParameter(
                "parent",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                examples=[
                    OpenApiExample(
                        "Parent identifier",
                        summary="Parent identifier",
                        value="POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=non-tech-team",
                    )
                ],
            ),
            OpenApiParameter(
                "child",
                OpenApiTypes.STR,
                OpenApiParameter.PATH,
                examples=[
                    OpenApiExample(
                        "Child identifier",
                        summary="Child identifier",
                        value="POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=sales-team",
                    )
                ],
            ),
        ]


class HRelV1Doc:
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
                "HRel - List All",
                value=[
                    {
                        "identifier": "POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=non-tech-team",
                        "type": "Team",
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
                        "HRel - Get",
                        summary="HRel Identifier",
                        description="HRel - Get",
                        value="POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=non-tech-team",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "HRel - Get",
                value={
                    "identifier": "POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=non-tech-team",
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
                "HRel - Create (Non Tech)",
                value={
                    "identifier": "POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=non-tech-team",
                    "type": "Team",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "HRel - Create (Sales)",
                value={
                    "identifier": "POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=sales-team",
                    "type": "Team",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "HRel - Create",
                value={
                    "identifier": "POLICY_TYPE=actor,POLICY_NAME=Team,TEAM=non-tech-team",
                    "type": "Team",
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
                        "HRel - Delete",
                        summary="HRel Identifier",
                        description="HRel - Delete",
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
                        "HRel - Patch",
                        summary="HRel Identifier",
                        description="HRel - Patch",
                        value="EXCHANGE=kubefacets.exchange",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "HRel - Patch",
                value={
                    "name": "kubefacets.exchange.v1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "HRel - Patch",
                value={
                    "identifier": "EXCHANGE=kubefacets.exchange.v1",
                    "name": "kubefacets.exchange.v1",
                    "attrs": {"durable": True, "exchange_type": "direct"},
                },
                request_only=False,
                response_only=True,
            ),
        ]
