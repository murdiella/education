import logging
import sys

logger = logging.getLogger("applicants")


def send_applicant_profile_to_university(applicant, soap_service):

    person = applicant.person

    address = person.address

    passport = person.passport

    personal_data = {
        "Email": applicant.user.email,
        "FirstName": person.firstname,
        "SecondName": person.middlename,
        "LastName": person.lastname,
        "BirthDate": person.date_of_birth.strftime("%Y-%m-%d"),
        "Sex": "000000001" if person.gender == person.MALE else "000000002",
        "Citizenship": applicant.citizenship.code,
        "PhoneMobile": person.phone,
        "PhoneHome": "",
        "SNILS": None,
        "Language": translate_language(applicant.language),
        "BirthPlace": person.place_of_birth,
    }

    passport_data = {
        "PassportType": "000000047",
        "Series": passport.series,
        "Number": passport.number,
        "KemVydan": passport.issuer,
        "DataVydachi": passport.issued_date.strftime("%Y-%m-%d"),
        "DepartamentCode": passport.issuer_code,
    }

    if not address:
        address = ""

    address_data = {
        "Homeless": person.no_address,
        "Country": address and applicant.citizenship.code,
        "City": address and address.city,
        "Region": address and address.region,
        "Area": address and address.district,
        "Town": address and address.township,
        "Street": address and address.street,
        "House": address and address.house,
        "Korpus": address and address.building,
        "Kvartira": address and address.apartment,
        "PostalIndex": address and address.zipcode,
        "KLADRCode": "",
    }

    result = soap_service.service.CreateReplaceAnketa(
        AbiturientCode=applicant.ref or "",
        OsnovnyeDannye=personal_data,
        Passport=passport_data,
        RegistrationAddres=address_data,
    )

    logger.info(result)

    complete = result["UniversalResponse"]["Complete"]

    if not complete:
        message = result["UniversalResponse"]["Description"]
        raise ValueError(
            "CreateReplaceAnketa request was not complete %s" % message
        )
    else:
        code = result["AbiturientCode"]
        applicant.ref = code
        applicant.save()

    social_links = ", ".join(person.social_links.all())

    form47 = {
        "AbiturientCode": applicant.ref,
        "SocialNetwork": social_links,
        "Email": applicant.user.email,
        "Phone": person.phone,
        "City": "",
        "NeedRoom": applicant.preliminary_form.need_dormitory,
        "ConsentToNewsletter": False,
        "School": applicant.educations.first().name,
        "Language": translate_language(applicant.language),
    }

    specialities = {
        "StringNapravleniya": [
            {
                "EducationFormCode": "О00000000",
                "EducationLevelCode": "000000004",
                "FinanceCode": "000000003",
                "Loyalty": "",
                "SpecialityCode": selected_speciality.speciality.system_code,
                "Language": "",
            }
            for selected_speciality in applicant.selected_specialities.all()
        ],
    }

    data = {
        "Form47": form47,
        "Passport": passport_data,
        "Napravleniya": specialities,
    }

    ege = applicant.exams.all()

    if ege:
        data["EGE"] = {
            "StringEGE": [
                {
                    "PredmetCode": translate_code(exam.subject),
                    "Ball": exam.mark,
                }
                for exam in ege
            ],
        }

    result = soap_service.service.CreateForm47(**data)

    logger.info(result)
    print(result, file=sys.stderr)

    complete = result["Complete"]

    if not complete:
        message = result["Description"]
        raise ValueError("CreateForm47 request was not complete %s" % message)

    applicant.preliminary_form.sent = True
    applicant.preliminary_form.save()


def translate_code(subject):

    code_map = {
        "RU": "000000001",
        "MT": "000000002",
        "GE": "000000003",
        "HS": "000000005",
        "SC": "000000006",
        "PH": "000000008",
        "EN": "000000010",
        "FR": "000000011",
        "GM": "000000012",
        "SP": "000000013",
        "IT": "000000014",
        "FO": "000000016",
        "CN": "000000017",
    }

    return code_map[subject]


def translate_language(language):

    translate_map = {
        "EN": "000000003",
        "FR": "000000006",
        "GE": "000000005",
    }

    return translate_map[language]
