from rest_framework import permissions


class IsAuthenticatedAndVerified(permissions.BasePermission):
    message = ""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            if request.user.is_email_verified is False:
                self.message = "Please verify your email address."
                return False
            elif request.user.is_verified is False:
                self.message = "Please verify your payment method."
                return False

            method = request.method
            if method == "PUT" or method == "POST" or method == "PATCH" or method == "DELETE":
                if request.auth.scope == request.auth.READ_SCOPE:
                    self.message = "You do not have permission to write."
                    return False

            return True

        return False
