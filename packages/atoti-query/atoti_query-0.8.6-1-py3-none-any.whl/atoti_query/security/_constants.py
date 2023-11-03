from collections.abc import Collection

# Keep this collection up to date with the roles in SecurityConstants.java.
SPECIAL_ROLES: Collection[str] = [
    "ROLE_USER",
    "ROLE_ADMIN",
    "ROLE_ATOTI_ROOT",
    "ROLE_CS_ROOT",
]
ROLE_USER = "ROLE_USER"
ROLE_ADMIN = "ROLE_ADMIN"
ROLE_ATOTI_ROOT = "ROLE_ATOTI_ROOT"
USER_CONTENT_STORAGE_NAMESPACE = "activeviam/content"
