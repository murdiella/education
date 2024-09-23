from apps.applicants.models import Education
from apps.applicants.services import fill_education
from django.shortcuts import redirect, render


def educations(request):

    applicant = request.user.applicant
    if not applicant.citizenship:
        return redirect("applicants:citizenship")
    try:
        education = applicant.educations.first()
    except Education.doesNotExist:
        education = Education(applicant=applicant)
    if education is None:
        education = Education(applicant=applicant)
    if request.method == "POST":
        data = request.POST
        education = fill_education(education, data)
        if education:
            return redirect("applicants:root")
    years = range(2021, 1980, -1)
    return render(
        request,
        "educations.html",
        {
            "education": education,
            "years": years,
        },
    )
