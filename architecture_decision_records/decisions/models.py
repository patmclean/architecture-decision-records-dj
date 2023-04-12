"""Decision Models."""
from django.db import models
from django.conf import settings
from django.urls import reverse


class Status(models.Model):
    """Status for filtering records."""

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # new
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        """Return Status name as string."""
        return self.name

    def get_status():
        """Return the default status for a new record."""
        return Status.objects.get(id=1)

    class Meta:
        verbose_name = "Status Option"


class Decision(models.Model):
    """Decision Record."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=False, null=False, default=Status.get_status)
    slug = models.SlugField(null=True, unique=True)
    stakeholder = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    context = models.TextField()
    decision_description = models.TextField(blank=True)
    consequence = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        """Return Decision Record title name as string."""
        return self.title

    class Meta:
        """Meta for Decisions."""

        verbose_name = "Decision Record"
        ordering = ["-id"]

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = f"ADR{self.id:04}"
    #     return super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        """Create the ADR number."""
        # Save your model in order to get the id
        super().save(*args, **kwargs)

        # Then implement the logic for the slug
        if not self.slug:
            self.slug = f"ADR{self.id:04}"
            # Call save() again in order to save the slug
            self.save()

    @property
    def author(self):
        """Return a user friendly author name."""
        return "".join([self.user.first_name, " ", self.user.last_name])

    def get_absolute_url(self):  # new
        """Sets the canonical URL for the model.."""
        return reverse("decision_record", kwargs={"slug": self.slug})


class RevisionComment(models.Model):
    """RevisionComment Record."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, blank=False, null=False)
    type = models.SmallIntegerField(default=0)  # 0 -> Version , 1 -> Comment
    content = models.CharField(max_length=2048)
    date_created = models.DateTimeField(auto_now_add=True)
    version = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        """Return Decision Record title name as string."""
        return self.content

    class Meta:
        """Meta for Decisions."""

        verbose_name = "Revision/Comment Record"
        ordering = ["-date_created"]

    def save(self, *args, **kwargs):
        """Create the Version number."""
        # Save your model in order to get the id

        # Then implement the logic for the version number
        if self.type == 0:
            self.version = RevisionComment.objects.filter(decision=self.decision, type=0).count() + 1
            # Call save() again in order to save the version number
        super().save(*args, **kwargs)

    @property
    def author(self):
        """Return a user friendly author name."""
        return "".join([self.user.first_name, " ", self.user.last_name])
