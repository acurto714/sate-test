from django.db import models

class TasksScheduler(models.Model):
    tasks_file = models.FileField(upload_to='files/%Y/%m/%d')
    raw_tasks = models.CharField(max_length=1000)
    best_schedule = models.CharField(max_length=1000)

    def get_or_create_raw_tasks(self):
        if not self.raw_tasks:
            # TODO: write code
            self.raw_tasks = [
                {"nombre": "foto cliente 1098", "recursos": ["camara", "disco", "proc"] , "ganancia": 9.2},
                {"nombre": "limpieza de disco", "recursos": ["disco"] , "ganancia": 0.4},
                {"nombre": "upgrade a v2.1", "recursos": ["proc"] , "ganancia": 2.9}
            ]
        return self.raw_tasks

    def get_or_create_best_schedule(self):
        if not self.best_schedule:
            tasks = self.get_or_create_raw_tasks()
            # TODO: write code
            self.best_schedule = tasks
        return self.best_schedule
