"""Tests for decision models."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..models import Status, Decision

TEST_AUTH_PWD = "098y7ty3fgv45nj!ki90u8yu"


class ModelTests(TestCase):
    """Test cases for decision models."""

    def test_create_status(self):
        """Test creating a status is successful."""
        status = Status.objects.create(name="Status1", slug="status1")

        self.assertEqual(str(status), status.name)

    def test_create_decision(self):
        """Test creating a decision is successful."""
        status = Status.objects.create(name="Status1", slug="status1")
        user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.ie",
            password=TEST_AUTH_PWD,
        )
        decision = Decision.objects.create(
            user=user,
            stakeholder="I am a stakeholder.",
            status=status,
            slug="i-am-a-slug",
            title="I am a title",
            context="Sample decision context",
            decision_description="Sample decision description.",
            consequence="Sample decision consequence.",
            date_created=timezone.now(),
        )

        self.assertEqual(str(decision), decision.title)
        self.assertEqual(status, decision.status)

    def test_create_revision(self):
        """Test creating a decision is successful."""
        status = Status.objects.create(name="Status1", slug="status1")
        user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.ie",
            password=TEST_AUTH_PWD,
        )
        decision = Decision.objects.create(
            user=user,
            stakeholder="I am a stakeholder.",
            status=status,
            slug="i-am-a-slug",
            title="I am a title",
            context="Sample decision context",
            decision_description="Sample decision description.",
            consequence="Sample decision consequence.",
            date_created=timezone.now(),
        )
        


        self.assertEqual(str(decision), decision.title)
        self.assertEqual(status, decision.status)

