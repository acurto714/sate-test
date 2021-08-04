from django.shortcuts import render
from .models import TasksScheduler
from .forms import TasksFileForm

import logging

logger = logging.getLogger(__name__)


def my_view(request):
    error = None
    if request.method == 'POST':
        form = TasksFileForm(request.POST, request.FILES)
        if form.is_valid():
            # import ipdb; ipdb.set_trace()
            sched = TasksScheduler(tasks_file=request.FILES["tasks_file"])
            sched.save()

            # TODO: review log
            logger.info("The schedule id: %d was created", sched.id)

            result = {
                "raw_tasks": sched.get_or_create_raw_tasks(),
                "best_schedule": sched.get_or_create_best_schedule(),
            }
            return render(request, 'result.html', result)
        else:
            error = 'The form is not valid. Fix the following error: '
    else:
        form = TasksFileForm()

    context = {'form': form, 'error': error}
    return render(request, 'upload.html', context)
