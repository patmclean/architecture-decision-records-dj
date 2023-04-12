"""Configuration for the Decisions App."""
from django.apps import AppConfig


class DecisionsConfig(AppConfig):
    """DecisionsConfig."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "architecture_decision_records.decisions"
