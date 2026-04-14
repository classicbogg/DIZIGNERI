from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("team_name", models.CharField(max_length=255)),
                ("course", models.CharField(max_length=255)),
                ("status", models.CharField(default="pending", max_length=50)),
                ("date_submitted", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-date_submitted",)},
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255)),
                ("is_captain", models.BooleanField(default=False)),
                (
                    "team_application",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="members", to="core.teamapplication"),
                ),
            ],
        ),
    ]