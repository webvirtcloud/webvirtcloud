from django import forms
from crispy_forms.helper import FormHelper
from region.models import Region
from compute.models import Compute


class CustomModelChoiceField(forms.ModelChoiceField):
    type_input = "select"

    def label_from_instance(self, item):
        return f"{item.name}"


class FormCompute(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormCompute, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["region"] = CustomModelChoiceField(
            queryset=Region.objects.filter(is_deleted=False)
        )
        self.fields["region"].empty_label = None

    class Meta:
        model = Compute
        fields = ["name", "arch", "description", "hostname", "token", "region"]


class FormStateAction(forms.Form):
    action = forms.ChoiceField(
        choices=[("start", "Start"), ("stop", "Stop")]
    )

    def __init__(self, *args, **kwargs):
        super(FormStateAction, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        if action not in ["start", "stop"]:
            raise forms.ValidationError("Invalid action")
        return cleaned_data


class FormStartAction(forms.Form):
    action = forms.ChoiceField(
        choices=[("autostart", "Autostart"), ("manualstart", "Manualstart")]
    )

    def __init__(self, *args, **kwargs):
        super(FormStartAction, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        if action not in ["autostart", "manualstart"]:
            raise forms.ValidationError("Invalid action")
        return cleaned_data
