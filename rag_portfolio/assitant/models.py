from django.db import models
from django.utils import timezone


class LLMStatus(models.Model):
    """Single row - global on/off switch for the whole app."""

    is_active = models.BooleanField(default=True)

    message = models.CharField(
        max_length=255,
        default="Server is down. Please try again later."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LLM Active: {self.is_active}"


class LLMUsageLog(models.Model):
    """One row per request - this is what powers the analytics dashboard."""

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    audio_seconds = models.FloatField(default=0)  # kept for future ASH/ASD, unused for text-only now

    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp} — {self.total_tokens} tokens"