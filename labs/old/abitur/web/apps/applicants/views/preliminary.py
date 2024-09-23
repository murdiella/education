from apps.applicants.models import Applicant, PreliminaryForm
from django.shortcuts import redirect, render


def preliminary(request):
    user = request.user
    applicant = Applicant.objects.get(user=user)
    try:
        preliminary_form = applicant.preliminary_form
    except PreliminaryForm.DoesNotExist:
        preliminary_form = PreliminaryForm(applicant=applicant)

    if request.method == "POST":
        data = request.POST
        preliminary_form.need_dormitory = (
            data.get("need_dormitory", False) == "on"
        )
        applicant.language = data["language"]
        preliminary_form.full_clean()
        applicant.ref = applicant.ref or None
        applicant.full_clean()
        preliminary_form.save()
        applicant.save()
        return redirect("applicants:root")

    return render(
        request,
        "preliminary.html",
        {
            "preliminary_form": preliminary_form,
            "applicant": applicant,
        },
    )
