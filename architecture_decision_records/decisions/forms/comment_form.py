"""Basic Django form for Comments."""
from django import forms


class CommentForm(forms.Form):
    """I don't know WTF i am going to do here."""

    content = forms.CharField(widget=forms.Textarea)
