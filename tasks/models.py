import json
from django.db import models
from tasks.scheduler import get_highest_profit_schedule


class TasksScheduler(models.Model):
    tasks_file = models.FileField(upload_to="files/%Y/%m/%d")
    raw_tasks = models.JSONField(blank=True, null=True)
    best_schedule = models.JSONField(blank=True, null=True)

    def _get_raw_tasks(self):
        if not self.raw_tasks:
            self.raw_tasks = []
            with open(self.tasks_file.path, "+r") as file:
                json_file = json.loads(file.read())
                for task in json_file:
                    self.raw_tasks.append(task)
            self.save()
        return self.raw_tasks

    def _get_best_sched(self):
        if not self.best_schedule:
            raw_tasks = self._get_raw_tasks()
            tasks = raw_tasks.copy()
            self.best_schedule = get_highest_profit_schedule(tasks)
            self.save()
        return self.best_schedule

    def get_highest_profit_schedule(self) -> dict:  # pragma: no cover
        result = {
            "raw_tasks": self._get_raw_tasks(),
            "best_schedule": self._get_best_sched(),
        }
        return result
