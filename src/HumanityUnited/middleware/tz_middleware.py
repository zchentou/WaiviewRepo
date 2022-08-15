import pytz

from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone_to_use = request.user.profile.timezone_to_use
            if timezone_to_use:
                timezone.activate(pytz.timezone(timezone_to_use))
        else:
            timezone.activate(pytz.timezone('US/Eastern'))
        return self.get_response(request)
