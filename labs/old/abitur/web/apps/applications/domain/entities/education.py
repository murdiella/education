from datetime import date

from apps.utils.domain import Entity


class Certificate(Entity):

    issued_at: date
    organization: str
    number: str
    series: str
    document_type: int


class Education(Entity):
    """Models an education.

    Education is a concrete document, that confirms
    that given person have passed some educational
    process.
    """

    level: int
    certificate: Certificate
    year: int
    original: bool
