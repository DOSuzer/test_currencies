import pickle
from collections import deque
from datetime import datetime as dt

import redis
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from currency.settings import (
    APIKEY, INTERVAL, RECORDS, REDIS_HOST, REDIS_PORTT
)
from current.exceptions import TokenGetError
from current.serializers import USDCurrencyRatesSerializer


SERVICE_URL = 'https://openexchangerates.org/api/'
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORTT, db=0)
redis_client.set('last_request', dt.timestamp(dt.now()) - INTERVAL)


def get_currency_rate(pair: str, base: str) -> dict:
    """Получаем текущий обменный курс."""
    if not APIKEY:
        raise TokenGetError('Проверьте APIKEY в env')

    response = requests.get(
        SERVICE_URL + f'latest.json?app_id={APIKEY}&base={base}',
    )

    if response.status_code != 200:
        return {'error': 'external service error'}
    serializer = USDCurrencyRatesSerializer(data=response.json())
    if serializer.is_valid():
        return {base+pair: serializer.validated_data['rates'][pair]}
#    try:
#        exchange_rate = response.json().get('rates').get(pair)
#    except (AttributeError, KeyError):
#        return {'error': 'Pair not found!'}
    return {'error': 'Pair not found!'}


def get_previous_data(pair: str) -> deque:
    """Получаем данные предыдущих запросов."""
    raw_data = redis_client.get(pair)

    if not raw_data:
        raw_data = pickle.dumps(deque(RECORDS * [0], RECORDS))
        redis_client.set(pair, raw_data)

    return pickle.loads(raw_data)


@require_http_methods(['GET'])
def current_usd(request):
    """Вью функция получения курсов валютной пары USDRUB."""
    base = 'USD'
    currency = 'RUB'
    dq = get_previous_data(base + currency)
    now = dt.now()
    last_request_timestamp = float(redis_client.get('last_request'))

    if last_request_timestamp + INTERVAL >= dt.timestamp(now):
        old_data = list(dq)
        data = {base + currency: old_data[0]}
        data['previous_data'] = old_data
    else:
        data = get_currency_rate(currency, base)
        data['previous_data'] = list(dq)
        if data.get(base + currency):
            redis_client.set('last_request', dt.timestamp(now))
            dq.appendleft(data[base + currency])
            redis_client.set(base + currency, pickle.dumps(dq))

    return JsonResponse(data)
