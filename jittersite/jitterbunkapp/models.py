from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bunk(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    bunk_date = models.DateTimeField('date bunked')
    def __str__(self):
        return '{} -> {}'.format(
                self.from_user.username,
                self.to_user.username)
