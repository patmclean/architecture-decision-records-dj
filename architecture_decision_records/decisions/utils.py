"""utils for working with PDF output."""
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.response import TemplateResponse

from xhtml2pdf import pisa  # TODO: Change this when the lib changes.
import os
import posixpath
from io import BytesIO


class UnsupportedMediaPathException(Exception):
    """TODO Create exception handler."""

    pass


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf to retrieve Images,Stylesheets, etc.

    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    if uri.startswith("http://") or uri.startswith("https://"):
        return uri

    if settings.DEBUG:
        new_path = uri.replace(settings.STATIC_URL, "").replace(settings.MEDIA_URL, "")
        normalized_path = posixpath.normpath(new_path).lstrip("/")
        absolute_path = finders.find(normalized_path)
        if absolute_path:
            return absolute_path

    if settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        if not os.path.exists(path):
            for d in settings.STATICFILES_DIRS:
                path = os.path.join(d, uri.replace(settings.STATIC_URL, ""))
                if os.path.exists(path):
                    break
    else:
        raise UnsupportedMediaPathException(
            "media urls must start with %s or %s" % (settings.MEDIA_URL, settings.STATIC_URL)
        )
    return path


class PdfResponse(TemplateResponse):
    """Override the default render method to create our PDF."""

    def render(self):
        """Render the PDF file as {slug}.pdf and automatically down load it."""
        retval = super(PdfResponse, self).render()
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=%s" % (self.context_data["decision"].slug)
        self.headers = response
        result = BytesIO()
        pisa.CreatePDF(self.rendered_content, dest=result, link_callback=fetch_resources)
        self.content = result.getvalue()
        return retval


class PdfMixin(object):
    """A mixin got the CBV to allow for the creation of a pdf, using the slug."""

    response_class = PdfResponse
