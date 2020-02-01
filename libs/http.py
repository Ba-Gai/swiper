import json
from swiper import settings
from django.http import HttpResponse

def render_json(data=None, code=0):
    result = {
        'data': data,
        'code': code
    }
    # 如果在调试模式下
    if settings.DEBUG:
        json_result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
    # 如果在开发模式下
    else:
        # separators：分隔符，实际上是(item_separator, dict_separator)的一个元组，默认的就是(‘,’,’:’)；
        # 这表示dictionary内keys之间用“,”隔开，而KEY和value之间用“：”隔开。
        json_result = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=[',', ':'])

    return HttpResponse(json_result)