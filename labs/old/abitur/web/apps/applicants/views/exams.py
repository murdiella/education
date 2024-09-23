from apps.applicants.models import Exam
from django.shortcuts import redirect, render


def exams(request):
    applicant = request.user.applicant
    if not applicant.citizenship:
        return redirect("applicants:citizenship")
    if request.method == "POST":
        data = request.POST
        for exam in applicant.exams.all():
            exam.delete()
        marks = data.getlist("mark[]")
        subjects = data.getlist("subject[]")
        # TODO receive exams as a whole package
        if len(marks) < len(subjects):
            marks += [None] * (len(subjects) - len(marks))
        for subject, year, mark in zip(
            data.getlist("subject[]"),
            data.getlist("year[]"),
            marks,
        ):
            exam = Exam(
                applicant=applicant,
                subject=subject,
                year=year,
                mark=mark or None,
            )
            exam.save()
        return redirect("applicants:selected_specialities")
    years = range(2021, 1980, -1)
    return render(
        request,
        "exams.html",
        {
            "years": years,
        },
    )
