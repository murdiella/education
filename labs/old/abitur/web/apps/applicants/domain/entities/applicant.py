from typing import List, Optional

from apps.applicants.domain.values import Gender, Person
from apps.geography.domain.entities import Country
from apps.geography.domain.values import Address
from apps.utils.domain import Entity
from django.contrib.auth import get_user_model


class Applicant(Entity):
    """This entity models an applicant.

    Applicant is a concrete person (user of the system)
    that is applying to the university. Applicant may
    choose to apply multiple applications, but each
    application should be applied to unique admission
    campaign per applicant.

    Applicant cannot be instantiated without user. If no
    user is passed during instantiation of **new** applicant,
    TypeError is raised.

    Applicant encapsulates information about person:

    - Gender
    - Person
    - Address
    - Passport
    - Contacts
    - PersonalInfoProcessingAgreement
    """

    gender: Gender
    person: Person
    address: Address
    passport: Passport
    contacts: List[Contact]
    personal_info_processing_agreement: PersonalInfoProcessingAgreement
    citizenship: Optional[Country]

    def __init__(
        self,
        ref=None,
        citizenship=None,
        repository=None,
    ):
        if ref is None and user is None:
            raise TypeError(
                "New applicant cannot be instantiated without a user"
            )
        super().__init__(ref, repository)
        if citizenship is not None:
            self.citizenship = citizenship
