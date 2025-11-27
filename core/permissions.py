from rest_framework.permissions import BasePermission


def _resolve_owner(obj, lookup_path):
    current = obj
    for attr in lookup_path.split("__"):
        current = getattr(current, attr, None)
        if current is None:
            break
    return current


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff:
            return True

        lookup_path = getattr(view, "owner_lookup_field", None)
        if not lookup_path:
            return True

        owner = _resolve_owner(obj, lookup_path)
        return owner == user
