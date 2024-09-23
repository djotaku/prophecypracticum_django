"""A command to email someone who hasn't done their feedback."""

# run the command in cron.
# python_in_venv path/to/prophecypracticum manage.py prophet_nudge

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from practicumweb.models import Prophecy, WeeklyLink, ProphecyFeedback
from practicumweb.views import find_sunday

class Command(BaseCommand):
    help = "Find supplicants who haven't participated this week"

    def handle(self, *args, **options):
        sunday = find_sunday()
        week_name = sunday.strftime('%Y%m%d')
        prophecies = Prophecy.objects.get_queryset().filter(week_name=week_name, status="published")
        for prophecy in prophecies:
            feedback = ProphecyFeedback.objects.get_queryset().filter(prophecy=prophecy.id, week_name=week_name, status="published")
            if not feedback:
                print("No feedback!")
                send_mail('You have not yet completed your feedback for this week.',
                          'Sign in at http://prophecypracticum.ericmesa.com/accounts/login/ site to complete it.',
                          'prophecypracticum@ericmesa.com',
                          [prophecy.supplicant.email],
                          fail_silently=False)