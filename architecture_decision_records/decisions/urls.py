"""Urls for the decisions App."""
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("markdown/", views.MarkdownView.as_view(), name="markdown"),
    path("new/", login_required(views.DecisionCreateView.as_view()), name="decision_new"),
    path("<slug:slug>/pdf", login_required(views.DecisionPdfView.as_view()), name="decision_pdf"),
    path("<slug:slug>/edit", login_required(views.DecisionUpdateView.as_view()), name="decision_edit"),
    path("<slug:slug>/accept", login_required(views.AcceptDecision), name="decision_accept"),
    path("<slug:slug>/reject", login_required(views.RejectDecision), name="decision_reject"),
    path("<slug:slug>/supersede", login_required(views.SupersedeDecision), name="decision_supersede"),
    path("<slug:slug>/add_comment", login_required(views.CommentCreateView), name="decision_comment"),
    path("<slug:slug>", views.DecisionDetailView.as_view(), name="decision_record"),
    path("search/", views.SearchResultsListView.as_view(), name="search_results"),
]
