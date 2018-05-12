from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Label, Task, Comment


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['label_text', 'label_description', 'label_color']

    label_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    label_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    label_color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


class ProtocolParseForm(forms.Form):
    protocol_url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    protocol_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=False)

    def clean(self):
        check_form = super(ProtocolParseForm, self).clean()

        if not any(
            check_form.get(x, '')
            for x in (
                'protocol_url',
                'protocol_text',
            )
        ):
            self._errors['protocol_url'] = self.error_class([("You must enter at least the protocol url or text")])
            self._errors['protocol_text'] = self.error_class([("You must enter at least the protocol url or text")])


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'task_description', 'finished_date', 'assignedTo', 'labels', 'important', 'progress']

    task_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    task_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    #assignedTo = forms.MultiWidget(widget=forms.CheckboxSelectMultiple(attrs={'class':'js-example-basic-multiple'}))

    def clean_finished_date(self):
        finished = self.cleaned_data['finished_date']

        if finished < timezone.now().date():
            raise ValidationError("Date too early")

        return finished

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
