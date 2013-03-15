from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

# FIXME: this is completely stubbed out at this point!

class AcomAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        return True
        #if 'admin' in request.user.username:
        #  return True

        #return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class AcomAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True
        #if request.user.username == 'admin':
        #    return True
        #else:
        #    return False

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        #if request and hasattr(request, 'user'):
        #    return object_list.filter(author__username=request.user.username)
        #return object_list.none()
        return object_list.all()
