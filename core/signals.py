import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Record

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Record)
def log_record_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info("Record %s: id=%s", action, instance.pk)