from django.contrib.auth.models import User


class MasqueradeMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Checks for the presence of "mask_user" in the session. The value
        should be the username of the user to be masqueraded as. Note we
        also set the "is_masked" attribute to true in that case so that when we
        hit the "mask" or "unmask" URLs this user is properly recognized,
        rather than the user they're masquerading as :) """

        request.user.is_masked = False

        if 'mask_user' in request.session:
            try:
                request.user = \
                  User.objects.get(username=request.session['mask_user'])
                request.user.is_masked = True
            except User.DoesNotExist:
                pass

        return self.get_response(request)
