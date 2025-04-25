from rest_framework.throttling import SimpleRateThrottle


class UserRegistrationThrottle(SimpleRateThrottle):
    scope = "user_registration"

    def get_cache_key(self, request, view):
        # Ограничиваем по IP
        return self.get_ident(request)
