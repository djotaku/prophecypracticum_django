import random
from datetime import datetime, timedelta
from itertools import zip_longest

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404

from .forms import ProphecyForm, ProphecyRatingForm, RandomizeForm, PracticumNamesForm
from .models import Prophecy, ProphecyFeedback, WeeklyLink, PracticumNames


def find_sunday():
    """If today isn't Sunday, find the previous Sunday."""
    today = datetime.now()
    today_weekday = today.weekday()
    sunday = today
    if today_weekday != 6:
        while sunday.weekday() != 6:
            sunday -= timedelta(days=1)
    return sunday


@login_required
def new_prophecy(request):
    random_person = random.randint(0, 10)
    prophecy = None
    prophet = request.user

    if request.method == "POST":
        # A prophecy was posted
        prophecy_form = ProphecyForm(data=request.POST)
        weekly_selection_form = PracticumNamesForm(data=request.POST)
        if prophecy_form.is_valid() and weekly_selection_form.is_valid():
            # create it, but don't save to database yet
            prophecy = prophecy_form.save(commit=False)
            prophecy.prophet = prophet
            selected_week = weekly_selection_form.cleaned_data['practicum_week'].week_name
            print(f"{selected_week=}")
            week_query = WeeklyLink.objects.get_queryset().filter(prophet=prophet, week_name=selected_week)
            print(week_query[0])
            supplicant = week_query[0].supplicant
            prophecy.supplicant = supplicant
            prophecy.week_name = selected_week
            prophecy.save()
            messages.success(request, "Your prophecy has been saved.")
            if prophecy.status == "published":
                messages.success(request, "Your prophecy has been published.")
                send_mail('You have a prophecy to read',
                          'Sign in at http://prophecypracticum.ericmesa.com/accounts/login/ site to see it.',
                          'prophecypracticum@ericmesa.com',
                          [supplicant.email],
                          fail_silently=False)
    else:
        prophecy_form = ProphecyForm()
        weekly_selection_form = PracticumNamesForm()
    return render(request, 'practicum/create_prophecy.html',
                  {'new_prophecy': prophecy, 'prophecy_form': prophecy_form, "random": random_person,
                   'weekly_form': weekly_selection_form})


@login_required()
def home(request):
    user = request.user
    published_prophecies = Prophecy.objects.get_queryset().filter(status='published', prophet=user)
    draft_prophecies = Prophecy.objects.get_queryset().filter(status='draft', prophet=user)
    prophecies_for_me = Prophecy.objects.get_queryset().filter(status='published', supplicant=user)
    feedbacks = ProphecyFeedback.objects.get_queryset().filter(status='published')
    feedback_list = [feedback.prophecy for feedback in feedbacks]
    return render(request, 'practicum/home.html',
                  {'published_prophecies': published_prophecies,
                   'draft_prophecies': draft_prophecies,
                   'feedback_list': feedback_list,
                   'prophecies_for_me': prophecies_for_me, })


@login_required()
def detailed_prophecy(request, year, month, day, prophet, supplicant, status):
    prophecy = get_object_or_404(Prophecy, status=status, created__year=year, created__month=month,
                                 created__day=day, prophet=prophet, supplicant=supplicant)
    feedback = None
    feedback_status = None
    what_am_i = None
    if request.method == "POST":
        # Changes made to prophecy
        prophecy_form = ProphecyForm(data=request.POST)
        if prophecy_form.is_valid():
            # create it, but don't save to database yet
            new_status = request.POST["status"]
            new_prophecy_text = request.POST['prophecy_text']
            prophecy.status = new_status
            status = prophecy.status
            prophecy.prophecy_text = new_prophecy_text
            supplicant = prophecy.supplicant
            prophecy.save()
            messages.success(request, "Your prophecy has been saved.")
            if prophecy.status == "published":
                messages.success(request, "Your prophecy has been published.")
                send_mail('You have a prophecy to read',
                          'Sign in at http://prophecypracticum.ericmesa.com/accounts/login/ site to see it.',
                          'prophecypracticum@ericmesa.com',
                          [supplicant.email],
                          fail_silently=False)
    else:
        prophecy_form = ProphecyForm(instance=prophecy)
        what_am_i = "supplicant" if request.user == prophecy.supplicant else "prophet"
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
    feedback_status = None
    prophecy = Prophecy.objects.get_queryset().filter(id=prophecy_id)
    if request.method == "POST":
        # A feedback was posted
        feedback_form = ProphecyRatingForm(data=request.POST)
        week_name = prophecy[0].week_name

        if feedback_form.is_valid():
            # create it, but don't save to database yet
            feedback = feedback_form.save(commit=False)
            feedback.prophecy = prophecy[0]
            feedback.week_name = week_name
            feedback.save()
            if feedback.status == "published":
                prophet = prophecy[0].prophet
                send_mail('You have feedback on your prophecy',
                          'Sign in at http://prophecypracticum.ericmesa.com/accounts/login/ site to see it',
                          'prophecypracticum@ericmesa.com',
                          [prophet.email],
                          fail_silently=False)
    elif feedback_query := ProphecyFeedback.objects.get_queryset().filter(
        prophecy=prophecy[0].id
    ):
        feedback_form = ProphecyRatingForm(instance=feedback_query[0])
    else:
        feedback_form = ProphecyRatingForm()
    return render(request, 'practicum/create_feedback.html',
                  {'new_feedback': feedback, 'feedback_form': feedback_form,
                   "feedback_status": feedback_status, "prophecy": prophecy[0]})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def randomizer(request):
    if request.method == "POST":
        user_selection_form = RandomizeForm(data=request.POST)
        if user_selection_form.is_valid():
            users = user_selection_form.cleaned_data['participants']
            users_list = list(users)
            randomized_prophet_pool = random.sample(users_list, len(users_list))
            randomized_supplicant_pool = random.sample(users_list, len(users_list))
            combined_list = zip_longest(randomized_prophet_pool, randomized_supplicant_pool)
            sunday = find_sunday()
            week_name = sunday.strftime('%Y%m%d')
            pairs = {}
            for pair in combined_list:
                if pair[0] == pair[1]:
                    user_list_without_self = [user for user in users_list if user is not pair[0]]
                    new_supplicant = random.choice(user_list_without_self)
                    pairs[pair[0]] = new_supplicant
                    database_entry = WeeklyLink(sunday_date=sunday, prophet=pair[0],
                                                supplicant=new_supplicant,
                                                week_name=week_name)
                else:
                    database_entry = WeeklyLink(sunday_date=sunday, prophet=pair[0], supplicant=pair[1],
                                                week_name=week_name)
                    pairs[pair[0]] = pair[1]
                database_entry.save()
            weekly_name_entry = PracticumNames(week_name=week_name)
            weekly_name_entry.save()
            return render(request, 'practicum/randomize.html', {'pairs': pairs})
    else:
        user_selection_form = RandomizeForm()
        return render(request, 'practicum/randomize.html', {'user_selection_form': user_selection_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def status_check(request):
    prophecies_this_week = None
    feedbacks = None
    feedback_list = None
    linked_users = None
    incomplete_prophets = None
    week_name = ""
    if request.method == "POST":
        weekly_selection_form = PracticumNamesForm(data=request.POST)
        if weekly_selection_form.is_valid():
            week_name = weekly_selection_form.cleaned_data['practicum_week'].week_name
            prophecies_this_week = Prophecy.objects.get_queryset().filter(week_name=week_name)
            feedbacks = ProphecyFeedback.objects.get_queryset().filter(week_name=week_name)
            linked_users = WeeklyLink.objects.get_queryset().filter(week_name=week_name)
            complete_practicum_prophets = {prophecy.prophet for prophecy in prophecies_this_week}
            this_week_practicum_prophets = {link.prophet for link in linked_users}
            incomplete_prophets = this_week_practicum_prophets - complete_practicum_prophets
            feedback_list = [feedback.prophecy for feedback in feedbacks]
    else:
        weekly_selection_form = PracticumNamesForm()
    return render(request, 'practicum/statuscheck.html', {'prophecies_this_week': prophecies_this_week,
                                                          "week_name": week_name, 'feedbacks': feedback_list,
                                                          "selection_form": weekly_selection_form,
                                                          'linked_users': linked_users,
                                                          'incomplete_prophets': incomplete_prophets})

