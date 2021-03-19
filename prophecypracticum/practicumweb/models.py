from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Prophecy(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    prophecy_text = models.TextField()
    # prophecy_photo = models.FileField() - may want to use ImageField, but either way see ...takes a few steps in URL https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield
    feedback_rating = models.PositiveIntegerField()
    feedback_text = models.TextField()
    prophet = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="my_prophecies")
    supplicant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="received_prophecies")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f"A prophecy by {self.prophet} for {self.supplicant} created {self.created}."
