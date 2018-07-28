import os

from googleads import adwords

from django.conf import settings


adwords_client = adwords.AdWordsClient.LoadFromStorage(
    os.path.join(settings.BASE_DIR, 'googleads.yaml'))
targeting_idea_service = adwords_client.GetService(
      'TargetingIdeaService', version='v201806')


def get_keywords_level_deep(keyword):
    results = get_queries([keyword], settings.PAGE_SIZE)
    keywords = [res['KEYWORD_TEXT'] for res in results['data']]
    results['data'] += get_queries(
        keywords, len(keywords) ** 2)['data']
    return results


def get_keywords(keyword):
    results = get_queries([keyword], settings.PAGE_SIZE)
    return results



def get_queries(queries, resultNumber):
    selector = {
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'requestedAttributeTypes': [
            'KEYWORD_TEXT',
            'SEARCH_VOLUME',
            'AVERAGE_CPC'],
        'paging': {
            'startIndex': 0,
            'numberResults': resultNumber
        },
        'searchParameters': [{
            'xsi_type': 'RelatedToQuerySearchParameter',
            'queries': queries
        }]
    }

    results = []
    page = targeting_idea_service.get(selector)
    for result in page['entries']:
        attributes = {}
        for attribute in result['data']:
            if 'AVERAGE_CPC' == attribute['key']:
                attributes['AVERAGE_CPC'] =\
                     attribute['value']['value']['microAmount']
            else:
                attributes[attribute['key']] = getattr(
                    attribute['value'], 'value', '0')
        results.append(attributes)
    return {
        'total_entries': page['totalNumEntries'],
        'data': results
    }
