from django import http
from django.utils.translation import gettext as _

class AuthException(Exception):
    '''
        Base class for all of our exceptions. 

        Has no particular meaning, other than "the current user cannot currently access this resource".
    '''
    pass

class LoginRequired(AuthException):
    '''
    The user is not logged in, and must log in to access this resource.

    App developers are not expected to instantiate this directly. Call require_login() instead.

    Site developers should catch this and provide the user with the opportunity to log in.
    '''
    pass

class PermissionDenied(AuthException):
    '''
    Indicates that the user is logged in, but lacks some necessary permission.

    App developers should call require_permission() when checking for standard django permissions, but they may also raise this directly when performing other custom permission checks.
    '''
    def __init__(self, message=None):
        self.message = message

class NotCurrentlyAllowed(AuthException):
    '''
    DEPRECATED. We recommend using Conflict, instead.

    Indicates that the user has all necessary permissions, but that the request cannot be handled because of some other time-based/logic constraints.

    Site developers should catch this and display a generic error message to the user.
    '''
    def __init__(self, reason):
        self.reason = reason

class Conflict(AuthException):
    '''
    The operation couldn't proceed because of some type of conflicting state
    (registration window hasn't opened yet, you must delete related objects first, etc.). 

    Note that this could be thrown from anywhere (even model code).
    Expect the message to be presented directly to the end user.
    '''
    def __init__(self, message, code=None):
        '''
        message should fully decribe why action can't proceed,
        and, ideally, what user can do to fix it. 
        Expect message to be shown directly to the end user.
        It may be a translatable string.

        code may be set, and can be used by higher levels of code 
        (ie. view code) to differentiate between types of Conflicts and
        render more specific error message, if desired.
        '''
        self.message = message
        self.code = code
    def __str__(self):
        return str(self.message)

def require_login(request):
    if request.user.is_anonymous :
        raise LoginRequired()

def require_permissions(request, *permission_names):
    require_login(request)
    user = request.user
    for permission_name in permission_names :
        # TODO - if DEBUG, should we validate that permission_name is actually a valid permission name?
        if not user.has_perm(permission_name) :
            raise PermissionDenied()

class BaseMiddleware:
    '''
        A Middleware base class which site developers can extend, to make handling our exceptions easier.
    '''

    # Boilerplate, required by all middleware
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, LoginRequired) :
            return self.login_required(request, exception)
        if isinstance(exception, PermissionDenied) :
            return self.permission_denied(request, exception)
        if isinstance(exception, NotCurrentlyAllowed) :
            return self.not_currently_allowed(request, exception)
        if isinstance(exception, Conflict) :
            return self.conflict(request, exception)

    # Site developers should override these methods
    def login_required(self, request, exception):
        return http.HttpResponse(_('Login required.'), content_type='text/plain')
    def permission_denied(self, request, exception):
        return http.HttpResponse(_('Permission denied.'), content_type='text/plain', status=403)
    def not_currently_allowed(self, request, exception):
        return http.HttpResponse(f'{_("Not currently allowed")}: {exception.reason}', content_type='text/plain', status=403)

    def conflict(self, request, exception):
        '''
        This implementation likely doesn't need to be overridden.
        Conflicts may be caught by view code to provide specific error messaging.
        This implementation is probably good enough as a general fallback.

        Note - if using jsform, this response works well if you add the 
        following to your base javascript:

            addEventListener('jsformerror', function(e) {
                var r = e.detail;
                if (r.status == 409 && r.responseText) {
                    alert(r.responseText);
                    e.preventDefault();
                    e.target.removeAttribute('block-submissions');
                }
            });
        '''
        return http.HttpResponse(exception.message, content_type='text/plain', status=409)
