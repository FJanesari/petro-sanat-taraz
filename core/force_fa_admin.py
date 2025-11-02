from django.utils import translation


class ForceFarsiAdminLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            translation.activate('fa')
            request.LANGUAGE_CODE = 'fa'

        response = self.get_response(request)

        if request.path.startswith('/admin/'):
            response.headers['Content-Language'] = 'fa'

        return response
