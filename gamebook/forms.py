from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Page, Story


class StoryForm(forms.Form):
    error_css_class = "alert alert-danger"

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Titre"
    )

    def clean_title(self):
        data = self.cleaned_data['title']

        if data == "error":
            raise ValidationError(_('Validation Error !!'))

        return data


class PageForm(forms.Form):
    error_css_class = "alert alert-danger"

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Titre"
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Contenu"
    )

    def clean_content(self):
        data = self.cleaned_data['content']

        if data == "error":
            raise ValidationError(_('Validation Error !!'))

        return data

    def clean_title(self):
        data = self.cleaned_data['title']

        if data == "error":
            raise ValidationError(_('Validation Error !!'))

        return data


class ActionForm(forms.Form):
    error_css_class = "alert alert-danger"

    label = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Texte"
    )
    destination = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        story = kwargs.pop("story")
        super(ActionForm, self).__init__(*args, **kwargs)

        self.fields['destination'].queryset = Page.objects.filter(story=story)

    def clean_label(self):
        data = self.cleaned_data['label']

        if data == "error":
            raise ValidationError(_('Validation Error !!'))

        return data
