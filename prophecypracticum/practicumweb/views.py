from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .models import Prophecy, ProphecyFeedback
from django.contrib.auth.decorators import login_required
from .forms import ProphecyForm, ProphecyRatingForm


# Create your views here.
@login_required
def new_prophecy(request):
    prophecy = None

    if request.method == "POST":
        # A comment was posted
        prophecy_form = ProphecyForm(data=request.POST)
        if prophecy_form.is_valid():
            # create it, but don't save to database yet
            prophecy = prophecy_form.save(commit=False)
            supplicant = prophecy.supplicant
            prophecy.save()
            if prophecy.status == "published":
                send_mail('You have a prophecy to read',
                          'Sign in at the Prophecy Practicum site to see it.',
                          'prophecypracticum@ericmesa.com',
                          [supplicant.email],
                          fail_silently=False)
    else:
        prophecy_form = ProphecyForm()
    return render(request, 'practicum/create_prophecy.html',
                  {'new_prophecy': prophecy, 'prophecy_form': prophecy_form})


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
    else:
        feedback_form = ProphecyRatingForm()
    return render(request, 'practicum/create_feedback.html',
                  {'new_feedback': feedback, 'feedback_form': feedback_form, "prophecy": prophecy[0]})
