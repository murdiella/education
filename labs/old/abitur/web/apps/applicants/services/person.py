from datetime import datetime

from apps.applicants.models import (
    Passport,
    Person,
    PersonalDataProcessingAgreement,
    Phone,
    Social,
)
from apps.geography.models import Address
from django.db import transaction


@transaction.atomic
def create_or_update_person_data(person, data, source):
    lastname = data["lastname"]
    firstname = data["firstname"]
    middlename = data.get("middlename", "")
    date_of_birth = datetime.strptime(data["date_of_birth"], "%d.%M.%Y").date()
    gender = Person.MALE if data["gender"] == "1" else Person.FEMALE
    place_of_birth = data["place_of_birth"]
    phone = data["phone"]

    person.lastname = lastname
    person.firstname = firstname
    person.middlename = middlename
    person.date_of_birth = date_of_birth
    person.gender = gender
    person.place_of_birth = place_of_birth
    person.phone = "+" + phone

    person.full_clean()

    try:
        passport = Passport.objects.get(person=person)
    except Passport.DoesNotExist:
        passport = Passport(person=person)
    passport.series = data.get("series", "")
    passport.number = data["number"]
    passport.issuer = data.get("issuer", "")
    passport.issuer_code = data.get("issuer_code", "")
    passport.issued_date = datetime.strptime(
        data["issued_date"], "%d.%M.%Y"
    ).date()
    print(data)

    if data.get("no_address", False):
        person.no_address = True
    else:
        address = person.address or Address()
        address.region = data.get("region", "")
        address.district = data.get("district", "")
        address.city = data.get("city", "")
        address.township = data.get("township", "")
        address.zipcode = data.get("zipcode", "")
        address.street = data.get("street", "")
        address.house = data.get("house", "")
        address.building = data.get("building", "")
        address.apartment = data.get("apartment", "")
        address.full_clean()
        address.save()
        person.no_address = False
        person.address = address
    person.full_clean()
    person.save()
    passport.full_clean()
    passport.save()
    try:
        person.pd_agreement
    except PersonalDataProcessingAgreement.DoesNotExist:
        agreement = PersonalDataProcessingAgreement(person=person, ip=source)
        agreement.full_clean()
        agreement.save()

    for phone in person.additional_phones.all():
        phone.delete()
    for number in data.getlist("phones[]", []):
        phone = Phone(
            person=person,
            number=number,
        )
        phone.full_clean()
        phone.save()

    for link in data.getlist("social[]", []):
        social = Social(
            person=person,
            link=link,
        )
        social.full_clean()
        social.save()

    return person
