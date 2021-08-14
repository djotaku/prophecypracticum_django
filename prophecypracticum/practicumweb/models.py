from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Prophecy(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    prophecy_text = models.TextField()
    # prophecy_photo = models.FileField() - may want to use ImageField, but either way see ...takes a few steps in URL https://docs.djangoproject.com/en/3.1/ref/models/fields/#filefield
    prophet = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="my_prophecies")
    supplicant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="received_prophecies")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    week_name = models.CharField(max_length=8, default="00000000")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('practicumweb:detailed_prophecy', args=[self.created.year, self.created.month, self.created.day,
                                                               self.prophet.id, self.supplicant.id, self.status])

    def __str__(self):
        return f"A prophecy created at {self.publish.month}/{self.publish.day} {self.publish.year} UTC."


class ProphecyFeedback(models.Model):
    """Holds feedback for a particular prophecy."""
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    feedback_rating = models.PositiveIntegerField()
    feedback_text = models.TextField()
    prophecy = models.ForeignKey(Prophecy, on_delete=models.CASCADE, related_name="my_rating")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    week_name = models.CharField(max_length=8, default="00000000")
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'A rating for the prophecy {self.prophecy}.'


class WeeklyLink(models.Model):
    """Links prophet and supplicant for a week."""
    sunday_date = models.DateTimeField()
    prophet = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="prophecy_week")
    supplicant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="supplicant_week")
    week_name = models.CharField(max_length=8, default="00000000")
    objects = models.Manager()


class PracticumNames(models.Model):
    """Holds all the practicum week_names"""
    week_name = models.CharField(max_length=8, default="00000000")
    objects = models.Manager()
