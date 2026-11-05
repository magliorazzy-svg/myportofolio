"""Access rules for the API, kept out of the views on purpose.

Roles (Assignment 4): visitor < regular user < Editor < owner (superuser).
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

EDITOR_GROUP = "Editor"


def is_editor(user):
    """True for a logged-in account that belongs to the Editor group."""
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP).exists()


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Anyone may read; only the portfolio owner (superuser) may write."""

    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Read: everyone. PUT/PATCH: owner and Editor. POST/DELETE: owner only."""

    message = "Only the portfolio owner or an Editor can change this."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.method in ("PUT", "PATCH") and is_editor(request.user)
