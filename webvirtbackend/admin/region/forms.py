from django import forms
from crispy_forms.helper import FormHelper
from region.models import Region


class FormRegion(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormRegion, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = Region
        fields = ["name", "slug", "description"]
