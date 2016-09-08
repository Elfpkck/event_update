from django.db import models


class Event(models.Model):
    start_time = models.DateTimeField()
    is_published = models.BooleanField(
        default=True)
    external_id = models.PositiveIntegerField()

    def __str__(self):
        return '{}, {}'.format(self.external_id, self.start_time)