from django.db.models import Sum, Count
from django.db.models.functions import TruncMinute, TruncHour, TruncDate
from django.utils import timezone
from datetime import timedelta

from .models import LLMUsageLog


def get_current_rates():
    now = timezone.now()
    minute_qs = LLMUsageLog.objects.filter(timestamp__gte=now - timedelta(minutes=1))
    hour_qs = LLMUsageLog.objects.filter(timestamp__gte=now - timedelta(hours=1))
    day_qs = LLMUsageLog.objects.filter(timestamp__gte=now - timedelta(hours=24))

    return {
        "rpm": minute_qs.count(),
        "tpm": minute_qs.aggregate(t=Sum("total_tokens"))["t"] or 0,
        "itpm": minute_qs.aggregate(t=Sum("input_tokens"))["t"] or 0,
        "otpm": minute_qs.aggregate(t=Sum("output_tokens"))["t"] or 0,
        "rpd": day_qs.count(),
        "tpd": day_qs.aggregate(t=Sum("total_tokens"))["t"] or 0,
        "ash": hour_qs.aggregate(t=Sum("audio_seconds"))["t"] or 0,
        "asd": day_qs.aggregate(t=Sum("audio_seconds"))["t"] or 0,
    }


def get_last_30_min_series():
    start = timezone.now() - timedelta(minutes=30)
    return list(
        LLMUsageLog.objects.filter(timestamp__gte=start)
        .annotate(bucket=TruncMinute("timestamp"))
        .values("bucket")
        .annotate(requests=Count("id"), tokens=Sum("total_tokens"))
        .order_by("bucket")
    )


def get_today_hourly_series():
    start = timezone.now() - timedelta(hours=24)
    return list(
        LLMUsageLog.objects.filter(timestamp__gte=start)
        .annotate(bucket=TruncHour("timestamp"))
        .values("bucket")
        .annotate(requests=Count("id"), tokens=Sum("total_tokens"))
        .order_by("bucket")
    )


def get_weekly_series():
    start = timezone.now() - timedelta(days=7)
    return list(
        LLMUsageLog.objects.filter(timestamp__gte=start)
        .annotate(bucket=TruncDate("timestamp"))
        .values("bucket")
        .annotate(requests=Count("id"), tokens=Sum("total_tokens"))
        .order_by("bucket")
    )