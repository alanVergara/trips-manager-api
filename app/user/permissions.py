from rest_framework import permissions


class IsPassengerOrAdmin(permissions.BasePermission):
    """Permission for action in passenger view"""
    def has_permission(self, request, view):
        admin_type = 1
        actions_admin = ['list']
        actions_free = ['create']

        if view.action in actions_free:
            return not request.user.is_authenticated
        elif view.action in actions_admin and request.user.is_authenticated:
            return request.user.user_type == admin_type
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Verification for specific instance actions"""
        actions_free = ['create']
        actions_passenger = ['retrieve', 'update', 'partial_update', 'destroy']

        if view.action in actions_free:
            return True
        elif (view.action in actions_passenger and
                request.user.is_authenticated):
            return obj == request.user


class IsDriverOrAdmin(permissions.BasePermission):
    """Permission for action in driver view"""
    def has_permission(self, request, view):
        admin_type = 1
        actions_admin = ['create', 'list', 'destroy']
        actions_driver = ['retrieve', 'update', 'partial_update']

        if view.action in actions_driver:
            return True
        elif view.action in actions_admin:
            return request.user.user_type == admin_type

    def has_object_permission(self, request, view, obj):
        """Verification for specific instance actions"""
        actions_driver = ['retrieve', 'update', 'partial_update']

        return (view.action in actions_driver and obj == request.user)
