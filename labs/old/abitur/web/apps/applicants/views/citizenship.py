from apps.applicants.models import Applicant
from apps.geography.models import Country
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def citizenship(request):
    user = request.user
    applicant = Applicant.objects.get(user=user)

    if request.method == "POST":
        code = request.POST["country_code"]
        # get the country by the code from the ORM repo
        # set applicant to the country
        # TODO restrict countries to have unique code
        country = Country.objects.filter(code=code).first()
        applicant.citizenship = country
        applicant.save()
        return redirect("applicants:root")

    countries = Country.objects.exclude(code="643")

    return render(
        request,
        "citizenship.html",
        {
            "citizenship": applicant.citizenship,
            "countries": countries,
        },
    )
