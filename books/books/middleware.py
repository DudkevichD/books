from django.shortcuts import redirect


class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == '/':
            return redirect('/admin/')
        response = self.get_response(request)
        return response
