import json


class RequestUrlPrintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.build_absolute_uri()
        query_params = request.GET.dict()

        body = request.body
        if request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
            if request.content_type and 'application/json' in request.content_type:
                try:
                    body = json.loads(request.body.decode('utf-8') or '{}')
                except (UnicodeDecodeError, json.JSONDecodeError):
                    body = request.body.decode('utf-8', errors='replace')
            else:
                if request.POST:
                    body = request.POST.dict()
                elif request.body:
                    body = request.body.decode('utf-8', errors='replace')

        print(
            f"{request.method} {url} | query={query_params} | body={body}",
            flush=True,
        )
        return self.get_response(request)