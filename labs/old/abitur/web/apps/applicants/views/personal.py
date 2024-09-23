from datetime import datetime

from apps.applicants.models import Person
from apps.applicants.services import create_or_update_person_data
from django.shortcuts import redirect, render


def personal(request):
    applicant = request.user.applicant
    if not applicant.citizenship:
        return redirect("applicants:citizenship")
    try:
        person = Person.objects.get(applicant=request.user.applicant)
    except Person.DoesNotExist:
        person = Person(applicant=request.user.applicant)

    if request.method == "POST":
        data = request.POST
        ip = request.META.get("REMOTE_ADDR")
        person = create_or_update_person_data(person, data, source=ip)
        return redirect("applicants:root")
    return render(
        request,
        "personal.html",
        {
            "person": person,
        },
    )
