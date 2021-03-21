from rest_framework import throttling


class PostOrderRateThrottle(throttling.UserRateThrottle):
    scope = 'post_order'

    def allow_request(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH']:
            return True
        return super().allow_request(request, view)
