from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RiddleSolution, SurvivorMachineCodeValidator, War, asm_max, bin_max


class SurvivorSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        war: War = kwargs.pop("war")
        amount_of_survivors = war.amount_of_survivors
        super(SurvivorSubmissionForm, self).__init__(*args, **kwargs)

        signature_validator = SurvivorMachineCodeValidator(competition=war.competition)

        for i in range(1, amount_of_survivors + 1):
            self.fields[f"asm_{i}"] = forms.FileField(label=_("Assembly source file: "), validators=[asm_max])
            self.fields[f"asm_{i}"].group = i
            self.fields[f"bin_{i}"] = forms.FileField(
                label=_("Binary file: "), validators=[bin_max, signature_validator]
            )
            self.fields[f"bin_{i}"].group = i


class RiddleSubmissionForm(forms.ModelForm):
    class Meta:
        model = RiddleSolution
        fields = ("riddle_solution",)
