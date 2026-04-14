from django.db import models


class ActiveRecordQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class RecordManager(models.Manager):
    def get_queryset(self):
        return ActiveRecordQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Record(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RecordManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class TeamApplication(models.Model):
    team_name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="pending")
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_submitted",)

    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    team_application = models.ForeignKey(
        TeamApplication, on_delete=models.CASCADE, related_name="members"
    )
    full_name = models.CharField(max_length=255)
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        role = "Captain" if self.is_captain else "Member"
        return f"{self.full_name} ({role})"