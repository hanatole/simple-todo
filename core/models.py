from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=[("New", "New"), ("Doing", "Doing"), ("Done", "Done")]
    )
