from django import forms
from django.core.validators import FileExtensionValidator


class TasksFileForm(forms.Form):
    tasks_file = forms.FileField(
        label="Select tasks file",
        validators=[FileExtensionValidator(allowed_extensions=["json"])],
    )
