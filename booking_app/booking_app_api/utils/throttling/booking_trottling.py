from rest_framework.throttling import SimpleRateThrottle


class BookingThrottle(SimpleRateThrottle):
    scope = "bookingcreate"

    def get_cache_key(self, request, view):
        # Ограничиваем по IP
        return self.get_ident(request)
