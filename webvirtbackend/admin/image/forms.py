from django import forms
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from image.models import Image
from region.models import Region


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    type_input = "checkbox"

    def label_from_instance(self, item):
        return f"{item.name}"


class FormImage(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormImage, self).__init__(*args, **kwargs)
        self.fields["type"] = forms.ChoiceField(
            widget=forms.Select, choices=Image.TYPE_CHOICES, initial=Image.DISTRIBUTION
        )
        self.fields["distribution"] = forms.ChoiceField(
            widget=forms.Select, choices=Image.DISTRO_CHOICES, initial=Image.UBUNTU
        )
        self.fields["regions"] = CustomModelMultipleChoiceField(
            queryset=Region.objects.filter(is_deleted=False), 
            widget=forms.CheckboxSelectMultiple()
        )
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "name", "slug", "type", "description", "md5sum", "distribution", 
            InlineCheckboxes("regions", css_class="checkboxinput"),
            "file_name",
        )

    class Meta:
        model = Image
        fields = "__all__"
