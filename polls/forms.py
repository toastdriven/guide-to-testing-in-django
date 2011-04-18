from django import forms
from polls.models import Choice


class PollForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # We require an ``instance`` parameter.
        self.instance = kwargs.pop('instance')
        
        # We call ``super`` (without the ``instance`` param) to finish
        # off the setup.
        super(PollForm, self).__init__(*args, **kwargs)
        
        # We add on a ``choice`` field based on the instance we've got.
        # This has to be done here (instead of declaratively) because the
        # ``Poll`` instance will change from request to request.
        self.fields['choice'] = forms.ModelChoiceField(queryset=Choice.objects.filter(poll=self.instance.pk), empty_label=None, widget=forms.RadioSelect)
    
    def save(self):
        if not self.is_valid():
            raise forms.ValidationError("PollForm was not validated first before trying to call 'save'.")
        
        choice = self.cleaned_data['choice']
        choice.record_vote()
        return choice
