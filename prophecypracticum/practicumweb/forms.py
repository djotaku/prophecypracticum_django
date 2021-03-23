from django import forms
from .models import Prophecy, ProphecyFeedback


class ProphecyForm(forms.ModelForm):
    class Meta:
        model = Prophecy
        fields = ('prophecy_text', 'prophet', 'supplicant', 'status',)


class ProphecyRatingFrom(forms.ModelForm):
    class Meta:
        model = ProphecyFeedback
        fields = ('feedback_rating', 'feedback_text', 'status')
