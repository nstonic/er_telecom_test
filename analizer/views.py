import json
from http import HTTPStatus

from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from analizer.services import get_function, collect_modules


@require_http_methods(["POST"])
def analize(request: HttpRequest):
    post_data = request.body.decode(encoding='utf8')

    if not post_data:
        returned_data = {'error': 'No data posted'}
        status = HTTPStatus.BAD_REQUEST
    else:
        serialized_json = json.loads(post_data)
        try:
            function = get_function(serialized_json)
        except (TypeError, ValueError, ImportError) as ex:
            returned_data = {'error': str(ex)}
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            returned_data = function(serialized_json)
            status = HTTPStatus.OK

    return JsonResponse(
        returned_data,
        status=status,
    )


@require_http_methods(["GET"])
def list_modules(request):
    modules = collect_modules(settings.MODULES_DIR)
    return render(request, 'analizer/index.html', context={'modules': modules})
