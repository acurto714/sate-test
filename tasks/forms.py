from django import forms  # pragma: no cover
from django.core.validators import FileExtensionValidator  # pragma: no cover


class TasksFileForm(forms.Form):  # pragma: no cover
    tasks_file = forms.FileField(
        label="Select tasks file",
        validators=[FileExtensionValidator(allowed_extensions=["json"])],
    )
