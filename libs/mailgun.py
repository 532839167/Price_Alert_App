import os
from typing import List
from requests import Response, post


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_API_KEY = '2e48452008ef72280d951f253bf73f6d-2a9a428a-4df8e65b'
    MAILGUN_DOMAIN = 'sandbox1159de262e3946499a11065d4e096df8.mailgun.org'

    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = f'do-not-reply@{MAILGUN_DOMAIN}'

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(gettext('mailgun_failed_load_api_key'))

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(gettext('mailgun_failed_load_domain'))

        response = post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text,
                'html': html,
            },
        )
        if response.status_code != 200:
            # print(response.status_code)
            # print(response.json())
            raise MailGunException('An error occurred while sending e-mail.')
        return response
