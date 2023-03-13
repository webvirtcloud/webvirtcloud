from django import forms
from crispy_forms.layout import Layout, Field
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes

from size.models import Size
from region.models import Region


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    type_input = "checkbox"

    def label_from_instance(self, item):
        return f"{item.name}"


class FormSize(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormSize, self).__init__(*args, **kwargs)
        self.fields["regions"] = CustomModelMultipleChoiceField(
            queryset=Region.objects.filter(is_deleted=False), 
            widget=forms.CheckboxSelectMultiple()
        )
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "name", "slug", "description", "vcpu", "disk", "memory", "transfer", "price",
            InlineCheckboxes("regions", css_class="checkboxinput")
        )

    class Meta:
        model = Size
        fields = "__all__"
