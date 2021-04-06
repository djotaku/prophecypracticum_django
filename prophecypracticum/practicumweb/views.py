from django.shortcuts import render, get_object_or_404
from .models import Prophecy
from django.contrib.auth.decorators import login_required
from .forms import ProphecyForm


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
            prophecy.save()
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
    user = request.user
    prophecy = get_object_or_404(Prophecy, status=status, created__year=year, created__month=month,
                                 created__day=day, prophet=prophet, supplicant=supplicant)
    prophecy_form = ProphecyForm(instance=prophecy)
    return render(request, 'practicum/detailed_prophecy.html', {'prophecy': prophecy, 'status': status,
                                                                'prophecy_form': prophecy_form})
