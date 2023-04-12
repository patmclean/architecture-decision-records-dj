from django.db import migrations


def create_statuses(apps, schema_editor):
    Status = apps.get_model("decisions", "Status")
    statuses = [
        ["Proposed", "proposed"],
        ["Rejected", "rejected"],
        ["Accepted", "accepted"],
        ["Superseded", "superseded"],
    ]
    for status, slug in statuses:
        Status.objects.create(name=status, slug=slug)


class Migration(migrations.Migration):
    dependencies = [
        ("decisions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_statuses),
    ]
