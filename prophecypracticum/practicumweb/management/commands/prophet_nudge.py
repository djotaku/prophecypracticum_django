"""A command to email someone who hasn't done their prophecy."""

# run the command in cron.
# python_in_venv path/to/prophecypracticum manage.py prophet_nudge

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from practicumweb.models import Prophecy, WeeklyLink
from practicumweb.views import find_sunday

class Command(BaseCommand):
    help = "Find prophets who haven't participated this week"

    def handle(self, *args, **options):
        sunday = find_sunday()
        week_name = sunday.strftime('%Y%m%d')
        prophets_this_week = WeeklyLink.objects.get_queryset().filter(week_name=week_name)
        for item in prophets_this_week:
            prophecy = Prophecy.objects.get_queryset().filter(prophet=item.prophet_id, week_name=week_name, status="published")
            if not prophecy:
                print("No prophecy!")
                send_mail('You have not yet completed your prophecy for this week.',
                          'Sign in at http://prophecypracticum.ericmesa.com/accounts/login/ site to complete it.',
                          'prophecypracticum@ericmesa.com',
                          [item.prophet.email],
                          fail_silently=False)