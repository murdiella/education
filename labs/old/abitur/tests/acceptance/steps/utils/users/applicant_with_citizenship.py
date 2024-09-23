from .applicant import Applicant


class ApplicantWithCitizenship(Applicant):

    email: str
    password: str

    def __init__(self, context, email=None, password=None, citizenship="Российская Федерация"):
        super().__init__(context, email, password)
        self.set_citizenship(citizenship)
