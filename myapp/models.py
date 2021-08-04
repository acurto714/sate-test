import json
from django.db import models

class TasksScheduler(models.Model):
    tasks_file = models.FileField(upload_to='files/%Y/%m/%d')
    raw_tasks = models.JSONField(blank=True, null=True)
    best_schedule = models.JSONField(blank=True, null=True)

    def get_or_create_raw_tasks(self):
        if not self.raw_tasks:
            self.raw_tasks = []
            with open(self.tasks_file.path, '+r') as file:
                json_file = json.loads(file.read())
                for task in json_file:
                    self.raw_tasks.append(task)
            self.save()
        return self.raw_tasks

    def get_or_create_best_schedule(self):
        if not self.best_schedule:
            tasks = self.get_or_create_raw_tasks()
            # TODO: write code
            self.best_schedule = tasks
            # TODO: end the code
            self.save()
        return self.best_schedule
