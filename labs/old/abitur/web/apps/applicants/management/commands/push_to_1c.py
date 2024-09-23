import os
import urllib.parse

import zeep
from apps.applicants.models import Applicant, PreliminaryForm
from apps.applicants.services import send_applicant_profile_to_university
from django.core.management.base import BaseCommand
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Plugin
from zeep.transports import Transport


class MyLoggingPlugin(Plugin):
    def egress(self, envelope, http_headers, operation, binding_options):
        http_headers["SOAPAction"] = urllib.parse.quote(
            http_headers["SOAPAction"]
        )
        return envelope, http_headers


class Command(BaseCommand):
    help = "Push applicants data to 1C"

    def handle(self, *args, **options):
        wsdl = os.getenv("WSDL_URL")
        session = Session()
        user = os.getenv("WSDL_USER")
        password = os.getenv("WSDL_PASSWORD")
        session.auth = HTTPBasicAuth(user, password)
        client = zeep.Client(
            wsdl,
            transport=Transport(session=session),
            plugins=[MyLoggingPlugin()],
        )
        for applicant in Applicant.objects.all():
            try:
                preliminary_form = applicant.preliminary_form
            except PreliminaryForm.DoesNotExist:
                continue

            if not preliminary_form.sent:
                send_applicant_profile_to_university(applicant, client)
