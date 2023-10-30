from enum import Enum


class LookerAsset(Enum):
    """Looker assets"""

    CONNECTIONS = "connections"
    CONTENT_VIEWS = "content_views"
    DASHBOARDS = "dashboards"
    EXPLORES = "explores"
    FOLDERS = "folders"
    GROUPS_HIERARCHY = "groups_hierarchy"
    GROUPS_ROLES = "groups_roles"
    LOOKML_MODELS = "lookml_models"
    LOOKS = "looks"
    PROJECTS = "projects"
    USERS = "users"
    USERS_ATTRIBUTES = "users_attributes"
