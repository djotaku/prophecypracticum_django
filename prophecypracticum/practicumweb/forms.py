from django import forms
from .models import Prophecy, ProphecyFeedback, User


class ProphecyForm(forms.ModelForm):
    class Meta:
        model = Prophecy
        fields = ('prophecy_text', 'status',)


class ProphecyRatingForm(forms.ModelForm):
    class Meta:
        model = ProphecyFeedback
        fields = ('feedback_rating', 'feedback_text', 'status')


class RandomizedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class RandomizeForm(forms.Form):
    participants = RandomizedModelMultipleChoiceField(queryset=User.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple)
