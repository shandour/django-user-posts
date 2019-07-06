import json

from functools import lru_cache, wraps
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.db import transaction
from .models import Company


email_hunter_base_url = 'https://api.hunter.io/'
relevant_enrichment_company_fields = [
    'name', 'legalName', 'location', 'description', 'domain'
]


# courtesy of hponde:
# https://gist.github.com/Morreski/c1d08a3afa4040815eafd3891e16b945
def timed_cache(**timedelta_kwargs):
    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() + update_delta
        f = lru_cache(None)(f)

        @wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)
        return _wrapped
    return _wrapper


# devliverability unlikely to change in the nearest
# 3 months so cache the reults
@timed_cache(days=90)
def check_email(email):
    success = False
    site_down = False

    resp = requests.head(email_hunter_base_url)

    if not resp.ok:
        site_down = True
    else:
        resp = requests.get(
            f'{email_hunter_base_url}/v2/email-verifier?email={email}'
            f'&api_key={settings.EMAIL_HUNTER_API_KEY}'
        )

        if resp.ok:
            data = json.loads(resp.content)['data']
            if (
                    data['regexp']
                    and not data['gibberish']
                    and data['result'] != 'undeliverable'
            ):
                success = True

    return success, site_down


def process_company_data(data_to_process):
    data = {}
    for k, v in data_to_process.items():
        if k in relevant_enrichment_company_fields:
            data[k] = v
    return data


def process_clearbit_response(response):
    data = {}
    if not response:
        return data

    person = response.pop('person', None)
    if person:
        data['person'] = {}
        for k, v in person.items():
            if k == 'name':
                data['person']['first_name'] = v.get('givenName')
                data['person']['last_name'] = v.get('familyName')
            elif k == 'location':
                data['person']['location'] = v
        company = response.pop('company', None)
        if company:
            data['company'] = process_company_data(company)
    else:
        data['company'] = process_company_data(response)

    return data


def handle_nested_company_object(user, company_data):
    with transaction.atomic():
        if company_data:
            if company_data.get('id'):
                Company.objects.filter(
                    pk=company_data['id']).update(**company_data)
            else:
                company = Company.objects.create(**company_data)
                company.users.add(user)
