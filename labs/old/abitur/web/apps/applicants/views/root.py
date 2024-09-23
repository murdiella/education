from apps.applicants.models import (
    Applicant,
    Education,
    Person,
    PreliminaryForm,
)
from django.shortcuts import redirect, render


def root(request):
    user = request.user
    applicant, _ = Applicant.objects.get_or_create(user=user)
    try:
        return render(
            request,
            "applicant.html",
            {
                "preliminary_form": applicant.preliminary_form,
            },
        )
    except PreliminaryForm.DoesNotExist:
        pass
    if not applicant.citizenship:
        return redirect("applicants:citizenship")
    try:
        applicant.person
    except Person.DoesNotExist:
        return redirect("applicants:personal")
    if not applicant.educations.all():
        return redirect("applicants:educations")
    if not applicant.exams.all():
        return redirect("applicants:exams")
    if not applicant.selected_specialities.all():
        return redirect("applicants:selected_specialities")
    return redirect("applicants:preliminary")
