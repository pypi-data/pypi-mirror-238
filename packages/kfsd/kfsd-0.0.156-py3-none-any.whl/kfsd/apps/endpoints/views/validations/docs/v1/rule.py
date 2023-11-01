from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class RuleV1Doc:
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
                "Rule - List All",
                value=[
                    {
                        "identifier": "RULES=Permission,RULE=Is Employee",
                        "name": "Is Employee",
                        "values": ["can_view", "can_write", "can_delete"],
                        "rules": "RULES=Permission",
                        "type": "VALIDATE",
                        "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
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
                        "rules": "RULES=Permission",
                        "type": "VALIDATE",
                        "prefetch": [],
                        "expr": "request.user.attrs.is_active == True",
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
                        "Rule - Get",
                        summary="Rule Identifier",
                        description="Rule - Get",
                        value="RULES=Permission,RULE=Is Employee",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Rule - Get",
                value={
                    "identifier": "RULES=Permission,RULE=Is Employee",
                    "name": "Is Employee",
                    "values": ["can_view", "can_write", "can_delete"],
                    "rules": "RULES=Permission",
                    "type": "VALIDATE",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "anyOf": [
                        {"expr": "request.user.attrs.is_superuser == True"},
                        {"expr": "request.user.attrs.is_staff == True"},
                        {"expr": "request.ctx.org == 'Kubefacets'"},
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
                "Rule - Create",
                value={
                    "name": "Is Employee",
                    "values": ["can_view", "can_write", "can_delete"],
                    "rules": "RULES=Permission",
                    "type": "VALIDATE",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "anyOf": [
                        {"expr": "request.user.attrs.is_superuser == True"},
                        {"expr": "request.user.attrs.is_staff == True"},
                        {"expr": "request.ctx.org == 'Kubefacets'"},
                    ],
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Rule - Create",
                value={
                    "identifier": "RULES=Permission,RULE=Is Employee",
                    "name": "Is Employee",
                    "values": ["can_view", "can_write", "can_delete"],
                    "rules": "RULES=Permission",
                    "type": "VALIDATE",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "anyOf": [
                        {"expr": "request.user.attrs.is_superuser == True"},
                        {"expr": "request.user.attrs.is_staff == True"},
                        {"expr": "request.ctx.org == 'Kubefacets'"},
                    ],
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
                        "Rule - Delete",
                        summary="Rule Identifier",
                        description="Rule - Delete",
                        value="RULES=Permission,RULE=Is Employee",
                    )
                ],
            )
        ]

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
                        "Rule - Exec",
                        summary="Rule Identifier",
                        description="Rule - Exec",
                        value="POLICY_TYPE=Events,POLICY_NAME=Outbound,RULE=TBL_UPSERT",
                    )
                ],
            )
        ]

    @staticmethod
    def exec_view_examples():
        return [
            OpenApiExample(
                "Rule - Exec (SuperUser)",
                value={"upsert": {"meta": {"op": "CREATE"}}},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Rule - Exec (Staff)",
                value={
                    "user": {
                        "attrs": {
                            "is_superuser": False,
                            "is_staff": True,
                            "is_active": True,
                        }
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Rule - Exec (User)",
                value={
                    "user": {
                        "attrs": {
                            "is_superuser": False,
                            "is_staff": False,
                            "is_active": True,
                        }
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Rule - Exec (Ctx)",
                value={
                    "user": {"attrs": {"org": "Kubefacets"}},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Rule - Exec",
                value={"detail": ["can_view", "can_write", "can_delete"]},
                request_only=False,
                response_only=True,
            ),
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
                        "Rule - Patch",
                        summary="Rule Identifier",
                        description="Rule - Patch",
                        value="RULES=Permission,RULE=Is Employee",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Rule - Patch",
                value={
                    "name": "Is Employee",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Rule - Patch",
                value={
                    "identifier": "RULES=Permission,RULE=Is Employee",
                    "name": "Is Employee",
                    "values": ["can_view", "can_write", "can_delete"],
                    "rules": "RULES=Permission",
                    "type": "VALIDATE",
                    "prefetch": [{"var": "org", "expr": "request.user.attrs.org"}],
                    "anyOf": [
                        {"expr": "request.user.attrs.is_superuser == True"},
                        {"expr": "request.user.attrs.is_staff == True"},
                        {"expr": "request.ctx.org == 'Kubefacets'"},
                    ],
                },
                request_only=False,
                response_only=True,
            ),
        ]
