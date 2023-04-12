"""Decision Form Declaration."""
# from crispy_forms.helper import FormHelper
# from crispy_forms.bootstrap import FormActions
# from crispy_forms.layout import Layout, Submit, Field
from django import forms

from ..models import Status, Decision


class DecisionForm(forms.ModelForm):
    """Form for managing the Decision model adding/editing."""

    status = forms.ModelChoiceField(Status.objects.all().order_by("id"), disabled=True)
    slug = forms.CharField(disabled=True)

    class Meta:
        """DecisionForm Meta class."""

        model = Decision
        fields = [
            "title",
            "context",
            "decision_description",
            "consequence",
            "slug",
            "status",
            "stakeholder",
        ]
