from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Доступ к API — только для активных сотрудников.
    """

    message = "Доступ разрешён только активным сотрудникам."

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.is_active and user.is_staff
