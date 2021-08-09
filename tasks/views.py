from django.shortcuts import render
from django.http import HttpResponse
from .models import TasksScheduler
from .forms import TasksFileForm

TASKS_FILE_KEY = "tasks_file"


def schedule(request):
    error = None
    if request.method == "POST":
        form = TasksFileForm(request.POST, request.FILES)
        if form.is_valid():
            sched = TasksScheduler(tasks_file=request.FILES[TASKS_FILE_KEY])
            sched.save()
            try:
                result = sched.get_highest_profit_schedule()
            except Exception as e:
                return HttpResponse(e.msg)
            else:
                return render(request, "result.html", result)
        else:
            error = "The form is not valid. Fix the following error: "
    else:
        form = TasksFileForm()

    context = {"form": form, "error": error}
    return render(request, "upload.html", context)
