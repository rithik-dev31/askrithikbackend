from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from .models import LLMStatus, LLMUsageLog

RPM_LIMIT = 30          # requests per minute
RPD_LIMIT = 1_000       # requests per day
TPM_LIMIT = 8_000       # tokens per minute
TPD_LIMIT = 200_000     # tokens per day


def record_usage(usage, session_key=None):
    """Logs this request, then checks rolling-window limits and
    updates the global on/off switch accordingly."""

    LLMUsageLog.objects.create(
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        session_key=session_key,
    )

    status, _ = LLMStatus.objects.get_or_create(id=1)

    now = timezone.now()
    minute_qs = LLMUsageLog.objects.filter(timestamp__gte=now - timedelta(minutes=1))
    day_qs = LLMUsageLog.objects.filter(timestamp__gte=now - timedelta(hours=24))

    rpm = minute_qs.count()
    tpm = minute_qs.aggregate(total=Sum("total_tokens"))["total"] or 0
    rpd = day_qs.count()
    tpd = day_qs.aggregate(total=Sum("total_tokens"))["total"] or 0

    if rpm >= RPM_LIMIT or tpm >= TPM_LIMIT:
        status.is_active = False
        status.message = "Too many requests right now. Please wait about a minute and try again."
    elif rpd >= RPD_LIMIT or tpd >= TPD_LIMIT:
        status.is_active = False
        status.message = "Daily usage limit reached. Please try again later."
    else:
        status.is_active = True

    status.save()
    return status