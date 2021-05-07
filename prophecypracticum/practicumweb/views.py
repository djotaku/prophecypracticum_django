from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .models import Prophecy, ProphecyFeedback, WeeklyLink, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProphecyForm, ProphecyRatingForm
from datetime import datetime, timedelta
from itertools import zip_longest
import random


@login_required
def new_prophecy(request):
    prophecy = None
    prophet = request.user
    today = datetime.now()
    today_weekday = today.weekday()
    sunday = today
    if today_weekday != 6:
        while sunday.weekday() != 6:
            sunday -= timedelta(days=1)
    this_week_link = WeeklyLink.objects.get_queryset().filter(prophet=prophet, sunday_date__year=sunday.year,
                                                              sunday_date__month=sunday.month,
                                                              sunday_date__day=sunday.day)
    supplicant = this_week_link[0].supplicant

    if request.method == "POST":
        # A prophecy was posted
        prophecy_form = ProphecyForm(data=request.POST)
        if prophecy_form.is_valid():
            # create it, but don't save to database yet
            prophecy = prophecy_form.save(commit=False)
            prophecy.prophet = prophet
            prophecy.supplicant = supplicant
            prophecy.save()
            if prophecy.status == "published":
                send_mail('You have a prophecy to read',
                          'Sign in at http://http://prophecypracticum.ericmesa.com/accounts/login/ site to see it.',
                          'prophecypracticum@ericmesa.com',
                          [supplicant.email],
                          fail_silently=False)
    else:
        prophecy_form = ProphecyForm()
        random_person = random.randint(0, 10)
    return render(request, 'practicum/create_prophecy.html',
                  {'new_prophecy': prophecy, 'prophecy_form': prophecy_form, "random": random_person})


@login_required()
def home(request):
    user = request.user
    published_prophecies = Prophecy.objects.get_queryset().filter(status='published', prophet=user)
    draft_prophecies = Prophecy.objects.get_queryset().filter(status='draft', prophet=user)
    prophecies_for_me = Prophecy.objects.get_queryset().filter(status='published', supplicant=user)
    return render(request, 'practicum/home.html',
                  {'published_prophecies': published_prophecies,
                   'draft_prophecies': draft_prophecies,
                   'prophecies_for_me': prophecies_for_me})


@login_required()
def detailed_prophecy(request, year, month, day, prophet, supplicant, status):
    prophecy = get_object_or_404(Prophecy, status=status, created__year=year, created__month=month,
                                 created__day=day, prophet=prophet, supplicant=supplicant)
    feedback = None
    feedback_status = None
    what_am_i = None
    if request.method == "POST":
        # Changed from Draft to Published
        prophecy_form = ProphecyForm(data=request.POST)
        if prophecy_form.is_valid():
            # create it, but don't save to database yet
            new_status = request.POST["status"]
            new_prophecy_text = request.POST['prophecy_text']
            prophecy.status = new_status
            prophecy.prophecy_text = new_prophecy_text
            supplicant = prophecy.supplicant
            prophecy.save()
            if prophecy.status == "published":
                send_mail('You have a prophecy to read',
                          'Sign in at http://http://prophecypracticum.ericmesa.com/accounts/login/ site to see it.',
                          'prophecypracticum@ericmesa.com',
                          [supplicant.email],
                          fail_silently=False)
    else:
        prophecy_form = ProphecyForm(instance=prophecy)
        what_am_i = "prophet"
        if request.user == prophecy.supplicant:
            what_am_i = "supplicant"
        feedback_query = ProphecyFeedback.objects.get_queryset().filter(prophecy=prophecy.id)
        feedback = 0
        feedback_status = 0
        if feedback_query:
            feedback = feedback_query[0]
            feedback_status = feedback.status
    return render(request, 'practicum/detailed_prophecy.html', {'prophecy': prophecy, 'status': status,
                                                                'prophecy_form': prophecy_form,
                                                                'feedback': feedback,
                                                                'feedback_status': feedback_status,
                                                                'what_am_i': what_am_i})


@login_required
def new_feedback(request, prophecy_id):
    feedback = None
    prophecy = Prophecy.objects.get_queryset().filter(id=prophecy_id)

    if request.method == "POST":
        # A comment was posted
        feedback_form = ProphecyRatingForm(data=request.POST)
        if feedback_form.is_valid():
            # create it, but don't save to database yet
            feedback = feedback_form.save(commit=False)
            feedback.prophecy = prophecy[0]
            feedback.save()
            if feedback.status == "published":
                prophet = prophecy[0].prophet
                send_mail('You have feedback on your prophecy',
                          'Sign in at the Prophecy Practicum site to see it.',
                          'prophecypracticum@ericmesa.com',
                          [prophet.email],
                          fail_silently=False)
    else:
        feedback_form = ProphecyRatingForm()
    return render(request, 'practicum/create_feedback.html',
                  {'new_feedback': feedback, 'feedback_form': feedback_form, "prophecy": prophecy[0]})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def randomizer(request):
    if request.method == "POST":
        users = User.objects.get_queryset()
        randomized_prophet_pool = random.sample(list(users), len(list(users)))
        randomized_supplicant_pool = random.sample(list(users), len(list(users)))
        combined_list = zip_longest(randomized_prophet_pool, randomized_supplicant_pool)
        print(list(combined_list))
    return render(request, 'practicum/randomize.html')
