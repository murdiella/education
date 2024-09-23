from datetime import datetime


def fill_education(education, data):
    education.level = data["level"]
    education.document_type = data["document_type"]
    education.name = data["name"]
    education.series = data.get("series", "")
    education.number = data.get("number", "")
    if "issued_date" not in data or not data["issued_date"]:
        education.issued_date = None
    else:
        education.issued_date = datetime.strptime(
            data["issued_date"], "%d.%M.%Y"
        ).date()
    education.year = data["year"]
    education.full_clean()
    education.save()
    return education
