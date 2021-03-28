from django.shortcuts import render
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
    return render(request, 'practicum/home.html', {'published_prophecies': published_prophecies})
