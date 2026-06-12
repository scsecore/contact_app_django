import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import os

class MailtrapAPIBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        token = os.getenv("MAILTRAP_TOKEN")
        inbox_id = '4695054'          # found in Mailtrap URL e.g. /inboxes/1234567

        sent = 0
        for msg in email_messages:
            payload = {
                "to": [{"email": r} for r in msg.to],
                "from": {"email": msg.from_email},
                "subject": msg.subject,
                "text": msg.body,
            }
            response = requests.post(
                f'https://sandbox.api.mailtrap.io/api/send/{inbox_id}',
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            if response.status_code == 200:
                sent += 1
        return sent