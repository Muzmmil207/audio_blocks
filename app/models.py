import uuid

from django.db import models
from django.db.models import CASCADE, Model
from django.utils.translation import gettext_lazy as _


class Audio(Model):
    class AudioType(models.TextChoices):
        VOICE_Over = "vo", _("Voice Over")
        BACKGROUND_Music = "bg_music", _("Background Music")
        VIDEO_Music = "video_music", _("Video Music ")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
    )
    type = models.CharField(
        max_length=12,
        choices=AudioType.choices,
    )
    high_volume = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name=_("High Volume"),
        help_text=_("volume when this element is not overlapping with other audio element."),
    )
    low_volume = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name=_("Low Volume"),
        help_text=_("volume when this element is overlapping with other audio element."),
    )
    video_component_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Video Component ID"),
        help_text=_("video-component-id if type is video_music else null."),
    )
    url = models.FileField(
        blank=True,
        null=True,
        upload_to="audios/",
        verbose_name=_("Audio File"),
        help_text=_("video-component-id if type is video_music else null."),
    )

    class Meta:
        verbose_name_plural = "Audios"
        ordering = ["-pk"]

    def __str__(self):
        return "audio_file"


class AudioDuration(Model):
    audio_element = models.OneToOneField(
        Audio,
        on_delete=CASCADE,
        related_name="duration",
        blank=False,
        null=False,
    )
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
