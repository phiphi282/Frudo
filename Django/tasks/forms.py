from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Label, Task, Comment

class CreateLabelForm(forms.ModelForm):
    """This form class provides a django interface for creating a new label.

    Attributes:
        label_text: The name of the label
        label_description: The description of the label
        label_color: The color of the label
    """
    class Meta:
        model = Label
        fields = ['label_text', 'label_description', 'label_color']

    label_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    label_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    label_color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class ProtocolParseForm(forms.Form):
    """This form class provides a django interface for parsing a protocol and automatically adding correctly given todos.

    Attributes:
        protocol_url: The URL where a protocol to be parsed is located
        protocol_text: The text of a protocol that is pasted by hand
    """
    protocol_url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    protocol_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=False)

    def clean(self):
        """Checks whether at least a protocol_url or protocol_text is given.
        """
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
    """This form class provides a django interface for creating a new task.

    Attributes:
        task_text: The title of the newly created task
        task_description: The description of the newly created task
    """
    class Meta:
        model = Task
        fields = ['task_text', 'task_description', 'finished_date', 'assignedTo', 'labels', 'important', 'progress']

    task_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    task_description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    #assignedTo = forms.MultiWidget(widget=forms.CheckboxSelectMultiple(attrs={'class':'js-example-basic-multiple'}))

    def clean_finished_date(self):
        """This function checks that the due date of the newly created task is not before the current date.
        """
        finished = self.cleaned_data['finished_date']

        if finished < timezone.now().date():
            raise ValidationError("Date too early")

        return finished

class CreateCommentForm(forms.ModelForm):
    """This form class provides a django interface for creating a new comment.

    Attributes:
        comment_text: the text of the comment (i. e., the comment itself)
    """
    class Meta:
        model = Comment
        fields = ['comment_text']

    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
