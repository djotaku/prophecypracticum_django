from django import forms
from .models import Prophecy, ProphecyFeedback


class ProphecyForm(forms.ModelForm):
    class Meta:
        model = Prophecy
        fields = ('prophecy_text', 'status',)


class ProphecyRatingForm(forms.ModelForm):
    class Meta:
        model = ProphecyFeedback
        fields = ('feedback_rating', 'feedback_text', 'status')
