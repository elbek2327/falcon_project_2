# import logging
# import sys
#

# from django.http import HttpResponse, JsonResponse, Http404
# from django.template.response import TemplateResponse
# from django.core.exceptions import ValidationError
import re
from django.utils.cache import cc_delim_re, get_conditional_response, set_response_etag
from django.utils.http import parse_http_date_safe
# from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class RequestLoggingMiddleware:
    """This function works whenever user requests anything Goes to any page or thing within hmtl"""
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        print(f"Request method: {request.method}, \n Request headers: {request.headers} \n Request path: {request.path}")

        response = self.get_response(request)
        return response


class AutoLogoutMiddleWare:
    """User will be automatically logged out when the time comes"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activiy')
            if last_activity is not None:
                difference_time = (now() - now().fromisoformat(last_activity)).total_seconds()
                if difference_time > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('shop:product')

            request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response

#
# logger = logging.getLogger(__name__)
# class ExceptionMiddleware:
#     """This middleware is for handling Django exceptions such as error 404 or else"""
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         return self.get_response(request)
#
#     def process_exception(self, request, exception):
#         logger.error(f"Unhandled exception: {str(exception)}", exc_info = True)
#
#         is_api_request = request.path.startswith('/api') or request.headers.get('Accept') == 'application/json'
#
#         if is_api_request is not None:
#             if isinstance(exception, ValueError):
#                 return JsonResponse({'error': str(exception)}, status=400)
#
#             return JsonResponse({'error': str(exception)}, status=500)
#
#         if issubclass(exception, Http404):
#             return TemplateResponse(request,'404.html', status=404)
#
#         # Default to 500 page
#         return TemplateResponse(request, '500.html', status=500)


class SecurityMiddleware(MiddlewareMixin):
    """Security middleware"""
    def __init__(self, get_response):
        super().__init__(get_response)
        self.sts_seconds = settings.SECURE_HSTS_SECONDS
        self.sts_include_subdomains = settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
        self.sts_preload = settings.SECURE_HSTS_PRELOAD
        self.content_type_nosniff = settings.SECURE_CONTENT_TYPE_NOSNIFF
        self.redirect = settings.SECURE_SSL_REDIRECT
        self.redirect_host = settings.SECURE_SSL_HOST
        self.redirect_exempt = [re.compile(r) for r in settings.SECURE_REDIRECT_EXEMPT]
        self.referrer_policy = settings.SECURE_REFERRER_POLICY
        self.cross_origin_opener_policy = settings.SECURE_CROSS_ORIGIN_OPENER_POLICY

    def process_request(self, request):
        path = request.path.lstrip("/")
        if (
            self.redirect
            and not request.is_secure()
            and not any(pattern.search(path) for pattern in self.redirect_exempt)
        ):
            host = self.redirect_host or request.get_host()
            return HttpResponsePermanentRedirect(
                "https://%s%s" % (host, request.get_full_path())
            )

    def process_response(self, request, response):
        if (
            self.sts_seconds
            and request.is_secure()
            and "Strict-Transport-Security" not in response
        ):
            sts_header = "max-age=%s" % self.sts_seconds
            if self.sts_include_subdomains:
                sts_header += "; includeSubDomains"
            if self.sts_preload:
                sts_header += "; preload"
            response.headers["Strict-Transport-Security"] = sts_header

        if self.content_type_nosniff:
            response.headers.setdefault("X-Content-Type-Options", "nosniff")

        if self.referrer_policy:
            response.headers.setdefault(
                "Referrer-Policy",
                ",".join(
                    [v.strip() for v in self.referrer_policy.split(",")]
                    if isinstance(self.referrer_policy, str)
                    else self.referrer_policy
                ),
            )

        if self.cross_origin_opener_policy:
            response.setdefault(
                "Cross-Origin-Opener-Policy",
                self.cross_origin_opener_policy,
            )
        return response


class ConditionalGetMiddleware(MiddlewareMixin):
    """GET operation handler (
    """
    def process_response(self, request, response):

        if request.method != "GET":
            return response

        if self.needs_etag(response) and not response.has_header("ETag"):
            set_response_etag(response)

        etag = response.get("ETag")
        last_modified = response.get("Last-Modified")
        last_modified = last_modified and parse_http_date_safe(last_modified)

        if etag or last_modified:
            return get_conditional_response(
                request,
                etag=etag,
                last_modified=last_modified,
                response=response,
            )

        return response

    def needs_etag(self, response):
        """Return True if an ETag header should be added to response."""
        cache_control_headers = cc_delim_re.split(response.get("Cache-Control", ""))
        return all(header.lower() != "no-store" for header in cache_control_headers)
