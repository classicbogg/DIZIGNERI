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
