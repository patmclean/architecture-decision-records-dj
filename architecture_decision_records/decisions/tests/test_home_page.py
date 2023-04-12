"""Testing the home page."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, resolve

from ..views import HomePageView
from .. import models

TEST_AUTH_PWD = "098y7ty3fgv45nj!ki90u8yu"


class HomepageTests(TestCase):
    """Tests for the home page."""

    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)
        self.status = models.Status.objects.create(name="Status1", slug="status1")
        self.user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.ie",
            password=TEST_AUTH_PWD,
        )
        self.decision = models.Decision.objects.create(
            user=self.user,
            stakeholder="I am a stakeholder.",
            status=self.status,
            slug="i-am-a-slug",
            title="I am a title",
            context="Sample decision context",
            decision_description="Sample decision description.",
            consequence="Sample decision consequence.",
            date_created=timezone.now(),
        )

    def test_homepage_status_code(self):
        """Check Status code."""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """Check file name."""
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        """Check file contains the word Home."""
        self.assertContains(self.response, "Home")

    def test_homepage_does_not_contain_incorrect_html(self):
        """Confirm a posited error code is not on the page."""
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_homepage_url_resolves_homepage_view(self):
        """Validate the homepage url."""
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)

    def test_book_detail_view(self):
        """Validate the Decision detail url."""
        response = self.client.get(self.decision.get_absolute_url())
        no_response = self.client.get("/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.decision.title)
        self.assertTemplateUsed(response, "decision.html")
