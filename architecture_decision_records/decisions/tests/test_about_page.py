"""Testing the home page."""

from django.test import TestCase
from django.urls import reverse, resolve

from ..views import AboutPageView


class about_pageTests(TestCase):
    """Tests for the home page."""

    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_about_page_status_code(self):
        """Check Status code."""
        self.assertEqual(self.response.status_code, 200)

    def test_about_page_template(self):
        """Check file name."""
        self.assertTemplateUsed(self.response, "about.html")

    def test_about_page_contains_correct_html(self):
        """Check file contains the word Home."""
        self.assertContains(self.response, "About")

    def test_about_page_does_not_contain_incorrect_html(self):
        """Confirm a posited error code is not on the page."""
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_about_page_url_resolves_about_page_view(self):
        """Validate the about_page url."""
        view = resolve("/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
