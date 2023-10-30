"""
Functionality of authorization
"""

import re
import aiohttp


LINK = 'https://chill.services/api/'


async def fetch(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()

def check_phone(cont):
    """ Phone checking """
    return 11 <= len(str(cont)) <= 18

def pre_process_phone(cont):
    """ Phone number pre-processing """

    if not cont:
        return 0

    cont = str(cont)

    if cont[0] == '8':
        cont = '7' + cont[1:]

    cont = re.sub(r'[^0-9]', '', cont)

    if not cont:
        return 0

    return int(cont)

def check_mail(cont):
    """ Mail checking """
    return re.match(r'.+@.+\..+', cont) is not None


def detect_type(login):
    """ Detect the type of authorization """

    if check_phone(pre_process_phone(login)):
        return 'phone'

    if check_mail(login):
        return 'mail'

    return 'login'

async def auth(
    project: str,
    by: str,
    token: str,
    network: int = 0,
    ip: str = None,
    locale: str = 'en',
    login: str = None,
    social: int = None,
    user: str = None,
    password: str = None,
    name: str = None,
    surname: str = None,
    image: str = None,
    mail: str = None,
    utm: str = None,
    online: bool = False,
    check_password: bool = False,
):
    """ Auth """

    req = {
        'by': by,
        'token': token,
        'network': network,
        'ip': ip,
        'locale': locale,
        'project': project,
        'login': login,
        'social': social,
        'user': user,
        'password': password,
        'name': name,
        'surname': surname,
        'image': image,
        'mail': mail,
        'utm': utm,
        'online': online,
        'check_password': check_password,
    }

    res = await fetch(LINK + 'account/proj/', req)
    return res['user'], res['token'], res['new']

async def token(
    project: str,
    token: str,
    network: int = 0,
    utm: str = None,
    extra: dict = None,
    ip: str = None,
    locale: str = 'en',
    user_agent: str = None,
):
    """ Save token """

    if extra is None:
        extra = {}

    req = {
        'token': token,
        'network': network,
        'utm': utm,
        'extra': extra,
        'ip': ip,
        'locale': locale,
        'user_agent': user_agent,
        'project': project,
    }

    res = await fetch(LINK + 'account/proj_token/', req)
    return res['token'], res['user'], res['status']
