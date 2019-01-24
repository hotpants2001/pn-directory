import json

from django.http import HttpResponse
from django.views.generic.base import View

class ApiGetView(View):
    """Simple API endpoint that returns a json string"""
    EMPTY_RESPONSE = json.dumps(dict())

    def api_get(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        result = self.api_get(request, args, kwargs)
        if result:
            return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'))
        return HttpResponse(self.EMPTY_RESPONSE)
