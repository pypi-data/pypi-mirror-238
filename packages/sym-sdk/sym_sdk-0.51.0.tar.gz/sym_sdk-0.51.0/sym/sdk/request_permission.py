"""Models for defining permissions required to view or perform actions on Requests."""

from enum import Enum
from typing import List, Union
from uuid import UUID

from pydantic import BaseModel, validator


class PermissionLevel(str, Enum):
    """Represent basic Request permission categories in the Sym platform.

    PermissionLevels are defined in descending order of permissions. Each permission level includes all permission
    levels below it.
    """

    ADMIN = "admin"
    """Permissions are applied to admins only. Admins are allowed to do anything.
    (e.g. Use symflow CLI, run Flows, apply Terraform).
    """

    MEMBER = "member"
    """Permissions are applied to admins and members only. Members can run Flows and interact with Requests."""

    ALL_USERS = "all_users"
    """Permissions are applied to all users (admins, members and guests). Guests can approve/deny/revoke Requests, if the Flow is configured to allow guest interactions."""


class RequestPermission(BaseModel):
    """A class representing permissions required to view or act on Requests. If no permissions are specified, then admin permission is implied."""

    webapp_view: Union[PermissionLevel, List[UUID]]
    """Defines who is allowed to view a Request in the web app. If a :class:`~sym.sdk.request_permission.PermissionLevel`
    is provided, all users with matching permissions will be able to view the Request. If specific IDs are provided,
    only those users will be granted permission to see the Request. Admins can always view all Requests.
    Convert List[:class:`~sym.sdk.user.User`] to List[UUID] using :class:`~sym.sdk.user.user_ids()`.
    """

    approve_deny: Union[PermissionLevel, List[UUID]]
    """Defines who is allowed to approve or deny the Request. If a :class:`~sym.sdk.request_permission.PermissionLevel`
    is provided, all users with matching permissions will be able to approve or deny the Request. If specific IDs
    are provided, only those users will be granted permission to approve or deny the Request. Admins can always approve
    or deny all Requests.
    Convert List[:class:`~sym.sdk.user.User`] to List[UUID] using :class:`~sym.sdk.user.user_ids()`.
    """

    allow_self_approval: bool = False
    """Whether the requester may approve their own Request."""

    @validator("webapp_view", "approve_deny", pre=True)
    @classmethod
    def validate_list_of_uuids(cls, value):
        """Validate that the
        :class:`~sym.sdk.request_permission.RequestPermission.webapp_view` and
        :class:`~sym.sdk.request_permission.RequestPermission.approve_deny` fields are an expected value and type.

        Args:
            value: Value passed to
                :class:`~sym.sdk.request_permission.RequestPermission.webapp_view` or
                :class:`~sym.sdk.request_permission.RequestPermission.approve_deny`.

        Returns:
            A list of User IDs or PermissionLevel.

        Raises:
            ValueError: If validation is unsuccessful.
        """
        if not value:
            raise ValueError("Input cannot be empty")

        user_ids_message = "Use sym.sdk.user.user_ids() to convert List[User] to List[UUID]."

        if isinstance(value, List) and not (all(isinstance(uuid, UUID) for uuid in value)):
            raise ValueError(f"Invalid input. {user_ids_message}")

        if not isinstance(value, PermissionLevel) and not isinstance(value, List):
            raise ValueError(
                f"Invalid input. Must be a PermissionLevel or List[UUID]. {user_ids_message}"
            )

        return value
