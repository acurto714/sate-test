from django import forms


class TasksFileForm(forms.Form):
    tasks_file = forms.FileField(label='Select tasks file')
