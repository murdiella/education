from apps.applicants.models import SelectedSpeciality, Speciality
from django.shortcuts import redirect, render


def selected_specialities(request):
    applicant = request.user.applicant
    if not applicant.citizenship:
        return redirect("applicants:citizenship")
    if request.method == "POST":
        data = request.POST
        for speciality in request.user.applicant.selected_specialities.all():
            speciality.delete()
        for i in range(1, 8):
            speciality_pk = data.get(f"speciality[{i}]", None)
            if not speciality_pk:
                continue
            speciality = Speciality.objects.get(pk=speciality_pk)
            SelectedSpeciality(
                applicant=request.user.applicant,
                speciality=speciality,
            ).save()
        return redirect("applicants:root")

    specialities = Speciality.objects.order_by("code").all()
    return render(
        request,
        "specialities.html",
        {
            "specialities": specialities,
        },
    )
