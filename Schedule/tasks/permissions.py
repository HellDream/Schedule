from rest_framework.permissions import IsAuthenticated
MY_SAFE_METHODS = ['GET', 'PUT', 'OPTION', 'DELETE']


class MyIsAuthenticated(IsAuthenticated):
    message = 'You must be the owner of this task.'

    def has_object_permission(self, request, view, obj):
        if request.method in MY_SAFE_METHODS:
            return True
        return obj.user == request.user


