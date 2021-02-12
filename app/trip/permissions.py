from rest_framework import permissions


class IsAdminRoute(permissions.BasePermission):
    """"""
    def has_permission(self, request, view):
        admin_type = 1
        actions_admin = ['create', 'update', 'partial_update', 'destroy']

        if view.action in actions_admin:
            return (request.user.is_authenticated and request.user.user_type == admin_type)
        else:
            return True


class IsAdminBus(permissions.BasePermission):
    """"""
    def has_permission(self, request, view):
        admin_type = 1
        actions_admin = ['create', 'list', 'update', 'partial_update', 'destroy']

        if view.action in actions_admin:
            return (request.user.is_authenticated and request.user.user_type == admin_type)
        else:
            return True


class IsPassengerTicket(permissions.BasePermission):
    """"""
    def has_permission(self, request, view):
        passenger_type = 2
        actions_passenger = ['list','retrieve', 'update', 'partial_update']

        if view.action in actions_passenger:
            return (request.user.is_authenticated and request.user.user_type == passenger_type)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """"""
        actions_free = ['list', 'retrieve']
        actions_passenger = ['update', 'partial_update']

        if view.action in actions_free:
            return True
        elif view.action in actions_passenger and request.user.is_authenticated:
            return obj.passenger is None


class IsAdminProfile(permissions.BasePermission):
    """"""
    def has_permission(self, request, view):
        admin_type = 1
        return (request.user.is_authenticated and request.user.user_type == admin_type)
