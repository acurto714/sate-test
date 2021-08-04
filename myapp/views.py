from django.shortcuts import render
from .models import TasksScheduler
from .forms import TasksFileForm

TASKS_FILE_KEY = 'tasks_file'


def schedule(request):
    error = None
    if request.method == 'POST':
        form = TasksFileForm(request.POST, request.FILES)
        if form.is_valid():
            sched = TasksScheduler(tasks_file=request.FILES[TASKS_FILE_KEY])
            sched.save()

            # TODO: add log for created sched

            result = {
                'raw_tasks': sched.get_or_create_raw_tasks(),
                'best_schedule': sched.get_or_create_best_schedule(),
            }
            return render(request, 'result.html', result)
        else:
            error = 'The form is not valid. Fix the following error: '
    else:
        form = TasksFileForm()

    context = {'form': form, 'error': error}
    return render(request, 'upload.html', context)
