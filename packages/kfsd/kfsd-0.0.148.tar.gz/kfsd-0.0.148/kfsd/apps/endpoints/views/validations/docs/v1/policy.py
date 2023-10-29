from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class PolicyV1Doc:
    @staticmethod
    def exec_view_examples():
        return []

    @staticmethod
    def exec_view_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Policy - Exec",
                        summary="Policy Identifier",
                        description="Policy - Exec",
                        value="RULES=Permission,RULE=Is Employee",
                    )
                ],
            )
        ]

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
                "Policy - List All",
                value=[
                    {
                        "identifier": "POLICY_TYPE=Inbound,POLICY_NAME=Signal",
                        "name": "Signal",
                        "resources": [],
                        "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                        "rules": [
                            {
                                "identifier": "RULES=Permission,RULE=Is Superuser",
                                "name": "Is Superuser",
                                "values": ["can_view", "can_write", "can_delete"],
                                "rules": ["RULES=Permission"],
                                "anyOf": [
                                    {"expr": "request.user.attrs.is_superuser == True"},
                                    {"expr": "request.user.attrs.is_staff == True"},
                                    {"expr": "request.ctx.org == 'Kubefacets'"},
                                ],
                            },
                            {
                                "identifier": "RULES=Permission,RULE=Default",
                                "name": "Default",
                                "values": ["can_view"],
                                "rules": ["RULES=Permission"],
                                "expr": "request.user.attrs.is_active == True",
                            },
                        ],
                    },
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
                        "Policy - Get",
                        summary="Policy Identifier",
                        description="Policy - Get",
                        value="RULES=Permission",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Policy - Get",
                value={
                    "identifier": "RULES=Permission",
                    "name": "Permission",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "rules": [
                        {
                            "identifier": "RULES=Permission,RULE=Is Superuser",
                            "name": "Is Superuser",
                            "values": ["can_view", "can_write", "can_delete"],
                            "rules": ["RULES=Permission"],
                            "anyOf": [
                                {"expr": "request.user.attrs.is_superuser == True"},
                                {"expr": "request.user.attrs.is_staff == True"},
                                {"expr": "request.ctx.org == 'Kubefacets'"},
                            ],
                        },
                        {
                            "identifier": "RULES=Permission,RULE=Default",
                            "name": "Default",
                            "values": ["can_view"],
                            "rules": ["RULES=Permission"],
                            "expr": "request.user.attrs.is_active == True",
                        },
                    ],
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Policy - Create",
                value={
                    "name": "Permission",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Policy - Create",
                value={
                    "identifier": "RULES=Permission",
                    "name": "Permission",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "rules": [],
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
                        "Policy - Delete",
                        summary="Policy Identifier",
                        description="Policy - Delete",
                        value="RULES=Permission",
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
                        "Policy - Patch",
                        summary="Policy Identifier",
                        description="Policy - Patch",
                        value="RULES=Permission",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Policy - Patch",
                value={
                    "name": "Permission",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Policy - Patch",
                value={
                    "identifier": "RULES=Permission",
                    "name": "Permission",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "rules": [],
                },
                request_only=False,
                response_only=True,
            ),
        ]
