import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.generic import TemplateView

from analizer.module_runner import ModuleRunner


class AnalizerView(TemplateView):
    template_name = 'analizer/index.html'

    def post(self, request, *args, **kwargs):
        file = self.request.FILES.get('json-file')

        if not file:
            returned_data = {'error': 'No file'}
            status = HTTPStatus.BAD_REQUEST
        else:
            data = json.load(file)
            try:
                ModuleRunner().run(data)
            except (TypeError, ValueError, ImportError) as ex:
                returned_data = {'error': str(ex)}
                status = HTTPStatus.INTERNAL_SERVER_ERROR
            else:
                returned_data = data
                status = HTTPStatus.OK

        return JsonResponse(
            returned_data,
            status=status,
        )


def list_modules(request):
    pass
