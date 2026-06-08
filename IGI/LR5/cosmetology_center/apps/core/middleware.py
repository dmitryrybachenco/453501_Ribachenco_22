import logging
import pytz
from django.utils import timezone
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    """Middleware для логирования запросов"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(
            f"Request: {request.method} {request.path} - User: {request.user} - IP: {self.get_client_ip(request)}"
        )

        response = self.get_response(request)

        logger.info(f"Response: {response.status_code} for {request.path}")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AgeRestrictionMiddleware:
    """Middleware для проверки возраста"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'birth_date'):
            from datetime import date
            age = date.today().year - request.user.birth_date.year
            if request.user.birth_date.month > date.today().month or \
                    (request.user.birth_date.month == date.today().month and
                     request.user.birth_date.day > date.today().day):
                age -= 1

            if age < 18 and request.path.startswith('/clients/appointments/'):
                raise PermissionDenied("Доступ запрещен: требуется возраст 18+")

        return self.get_response(request)