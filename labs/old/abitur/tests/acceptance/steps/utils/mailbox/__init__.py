import requests
from collections import namedtuple
from django.core import mail


Letter = namedtuple("Letter", ["text", "html", "to"])


class Mailbox:

    def __init__(self, environment):
        self.environment = environment

    def get_last_email(self, email):
        if self.environment == "production":
            messages = requests.get(
                "http://mailcatcher:1080/messages",
            ).json()
            for message in messages[::-1]:
                recipients = " ".join(message["recipients"])
                if email in recipients:
                    id = message["id"]
                    text = requests.get(
                        f"http://mailcatcher:1080/messages/{id}.plain",
                    ).content.decode("utf-8")
                    html = requests.get(
                        f"http://mailcatcher:1080/messages/{id}.html",
                    ).content.decode("utf-8")
                    break
            else:
                return None
        else:
            pass
        return Letter(text, html, email)
