from django.contrib import admin
from .models import LLMStatus, LLMUsageLog


@admin.register(LLMStatus)
class LLMStatusAdmin(admin.ModelAdmin):

    list_display = (
        "is_active",
        "updated_at",
    )

@admin.register(LLMUsageLog)
class LLMUsageLogAdmin(admin.ModelAdmin):

    list_display = (
        "session_key",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "timestamp",
    )