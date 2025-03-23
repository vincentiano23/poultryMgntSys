from django.contrib.auth.middleware import get_user
from django.shortcuts import redirect
from django.contrib import messages

class PreventSessionHijackingMiddleware:
    """
    Middleware to prevent session hijacking by verifying user identity.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = get_user(request)
        if request.user.is_authenticated:
            if 'ip_address' not in request.session:
                request.session['ip_address'] = self.get_client_ip(request)
            if 'user_agent' not in request.session:
                request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
            if (request.session['ip_address'] != self.get_client_ip(request) or
                    request.session['user_agent'] != request.META.get('HTTP_USER_AGENT', '')):
                messages.error(request, "Session hijacking detected! You have been logged out.")
                request.session.flush()  
                return redirect('login')  

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extracts client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]  # Get first IP from list
        return request.META.get('REMOTE_ADDR')
