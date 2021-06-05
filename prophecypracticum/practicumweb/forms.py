from django import forms
from .models import Prophecy, ProphecyFeedback, User


def create_user_choices():
    users = User.objects.get_queryset()
    return [(user, f"{user.first_name} {user.last_name}") for user in users]


class ProphecyForm(forms.ModelForm):
    class Meta:
        model = Prophecy
        fields = ('prophecy_text', 'status',)


class ProphecyRatingForm(forms.ModelForm):
    class Meta:
        model = ProphecyFeedback
        fields = ('feedback_rating', 'feedback_text', 'status')


class RandomizeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RandomizeForm, self).__init__(*args, **kwargs)
        self.fields['participants'] = forms.MultipleChoiceField(choices=create_user_choices(),
                                                                widget=forms.CheckboxSelectMultiple)

    class Meta:
        fields = ('participants', )
