from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read for everyone (authenticated due to global IsAuthenticated), 
    write only for owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj can be Post or Comment; both have .author
        return getattr(obj, "author_id", None) == request.user.id
