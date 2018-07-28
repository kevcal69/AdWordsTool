from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, View

from . import adwords


ADWORDS_UTIL = {
    '0': adwords.get_keywords,
    '1': adwords.get_keywords_level_deep
}


class IndexView(TemplateView):
    template_name = 'core/index.html'


class GetResultsView(View):

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse('Bad Request', status=400)

        request_type = request.GET.get('requestType', None)

        if request_type is None:
            return HttpResponse('Request type is needed', status=400)

        util_fn = ADWORDS_UTIL.get(request_type, None)
        if not util_fn:
            return HttpResponse('Bad Request', status=400)

        keywords = request.GET.get('keywords', None)
        if keywords is None:
            return HttpResponse('Keyword is needed', status=400)

        results = util_fn(keywords)
        return JsonResponse(results)
