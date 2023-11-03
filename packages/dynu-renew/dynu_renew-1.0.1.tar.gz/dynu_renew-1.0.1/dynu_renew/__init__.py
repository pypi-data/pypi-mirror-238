"""dynu_renew module."""

from typing import Final

from requests import get
from ipify import get_ip
from ipify.exceptions import ServiceError

from dynu_renew.database import Database

UPDATE_URL: Final = 'https://api.dynu.com/nic/update'
DEFAULT_TIMEOUT: Final = 10


def renew_domains_ip():
    """Renew domains' IP addresses."""
    from instance.config import DYNU_DOMAINS, DYNU_USERNAME, DYNU_PASSWORD  # pylint: disable=import-outside-toplevel

    try:
        myip = get_ip()
    except ConnectionError as ex:
        raise ConnectionError('unable to reach the ipify service, most likely because of a network error') from ex
    except ServiceError as ex:
        raise ServiceError('ipify is having issues, so the request couldn\'t be completed') from ex

    for domain in DYNU_DOMAINS:
        with Database() as db:
            if not db.check_domain_ip(domain, myip):
                db.save_domain_ip(domain, myip)

        response = get(UPDATE_URL, params={
            'hostname': domain,
            'myip': myip
        }, auth=(DYNU_USERNAME, DYNU_PASSWORD), timeout=DEFAULT_TIMEOUT)

        if (response.status_code != 200) or (response.text.strip() not in ('good', 'nochg')):
            raise Exception(f'Error received from Dynu: {response.text}')  # pylint: disable=broad-exception-raised
