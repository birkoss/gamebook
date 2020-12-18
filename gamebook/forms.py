from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _



class StoryForm(forms.Form):
	error_css_class = "alert alert-danger"

	title = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label="Titre"
    )
	#template = forms.ModelChoiceField(queryset=LibraryTemplate.objects.all())

	def clean_title(self):
		data = self.cleaned_data['title']

		if data == "error":
			raise ValidationError(_('Validation Error !!'))

		return data
