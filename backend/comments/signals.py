from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CommentAttachment
from .tasks import resize_image_task


@receiver(post_save, sender=CommentAttachment)
def process_image_on_upload(sender, instance, **kwargs):
    if instance.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        resize_image_task.delay(instance.file.path)
