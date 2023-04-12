"""Decisions views."""
# import logging
# import json

# from django.contrib import messages
# from django.db.models import Q
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
# from django.contrib.messages.views import SuccessMessageMixin

# from .utils import PdfMixin

# from . import models

# from .forms.decision_form import DecisionForm
# from .forms.comment_form import CommentForm

# logger = logging.getLogger("adra.decisions.views")


# class HomePageView(ListView):
#     """Home page View."""

#     model = models.Decision
#     context_object_name = "decisions_list"
#     template_name = "home.html"
#     paginate_by = 5


# class AboutPageView(TemplateView):
#     """About page View."""

#     template_name = "about.html"


# class MarkdownView(TemplateView):
#     """About page View."""

#     template_name = "markdown.html"


# class DecisionPdfView(SuccessMessageMixin, PdfMixin, DetailView):
#     """Details PDF Creator."""

#     model = models.Decision
#     context_object_name = "decision"
#     template_name = "decision_to_pdf.html"
#     headers = {"HX-Trigger": json.dumps({"showMessage": f"PDF Downloaded."})}


# class DecisionDetailView(DetailView):
#     """Details about a decision record."""

#     model = models.Decision
#     context_object_name = "decision"
#     template_name = "decision.html"


# class SearchResultsListView(ListView):  # new
#     """Search page Results View."""

#     model = models.Decision
#     context_object_name = "decisions_list"
#     template_name = "home.html"
#     queryset = models.Decision.objects.filter(title__icontains="Proposed")
#     paginate_by = 5

#     def get_queryset(self):
#         """Search records for the specified filter."""
#         query = self.request.GET.get("q")
#         return models.Decision.objects.filter(
#             Q(title__icontains=query)
#             | Q(stakeholder__icontains=query)
#             | Q(context__icontains=query)
#             | Q(user__last_name__icontains=query)
#             | Q(user__first_name__icontains=query)
#         )


# class DecisionCreateView(CreateView):
#     """Create a new decision Record."""

#     model = models.Decision
#     template_name = "decision_new.html"
#     fields = ["title", "stakeholder", "context", "decision_description", "consequence"]
#     success_url = "/"

#     def form_valid(self, form):
#         """Check the validity of the form, and set the Revision History."""
#         form.instance.user = self.request.user
#         form.save()
#         models.RevisionComment.objects.create(
#             user=self.request.user,
#             content="The Decision Record was created successfully",
#             type=0,
#             decision=form.instance,
#         )
#         return super(DecisionCreateView, self).form_valid(form)


# class DecisionUpdateView(UpdateView):
#     """Create a new decision Record."""

#     model = models.Decision
#     template_name = "decision_edit.html"
#     form_class = DecisionForm

#     def form_valid(self, form):
#         """Check the validity of the form, and set the Revision History."""
#         content = f"The following fields were changed [{','.join(form.changed_data)}]"
#         models.RevisionComment.objects.create(user=self.request.user, content=content, type=0, decision=form.instance)
#         messages.success(self.request, "The Decision Record was updated successfully.")
#         return super(DecisionUpdateView, self).form_valid(form)


# def CommentCreateView(request, slug):
#     """Create a comment against the current decision record."""
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             decision = models.Decision.objects.get(slug=slug)
#             comment = models.RevisionComment.objects.create(
#                 user=request.user, content=form.cleaned_data["content"], type=1, decision=decision
#             )
#             comment.save()
#             return HttpResponse(
#                 status=204,
#                 headers={
#                     "HX-Trigger": json.dumps(
#                         {"commentListChanged": None, "showMessage": f"Comment '{comment.content}' added to {slug}."}
#                     )
#                 },
#             )
#     else:
#         form = CommentForm()
#     return render(
#         request,
#         "_comment.html",
#         {
#             "form": form,
#             "slug": slug,
#         },
#     )


# def AcceptDecision(request, slug):
#     """Accept the currently selected Decision."""
#     accepted_decision = get_object_or_404(models.Decision, slug=slug)
#     accepted_decision.status = get_object_or_404(models.Status, slug="accepted")
#     accepted_decision.save()
#     models.RevisionComment.objects.create(
#         user=request.user, content="Decision was accepted", type=0, decision=accepted_decision
#     )
#     response = redirect(request.META.get("HTTP_REFERER"))
#     return response


# def RejectDecision(request, slug):
#     """Reject the currently selected Decision."""
#     rejected_decision = get_object_or_404(models.Decision, slug=slug)
#     rejected_status = get_object_or_404(models.Status, slug="rejected")
#     rejected_decision.status = rejected_status
#     rejected_decision.save()
#     models.RevisionComment.objects.create(
#         user=request.user, content="Decision was rejected", type=0, decision=rejected_decision
#     )
#     response = redirect(request.META.get("HTTP_REFERER"))
#     return response


# def SupersedeDecision(request, slug):
#     """Reject the currently selected Decision."""
#     superseded_decision = get_object_or_404(models.Decision, slug=slug)
#     superseded_decision.status = get_object_or_404(models.Status, slug="superseded")
#     superseded_decision.save()
#     models.RevisionComment.objects.create(
#         user=request.user, content="Decision was superseded", type=0, decision=superseded_decision
#     )
#     response = redirect(request.META.get("HTTP_REFERER"))
#     return response
