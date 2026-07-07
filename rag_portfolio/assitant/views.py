
from urllib import request

from django.shortcuts import render
from django.http import JsonResponse
from .models import LLMStatus
from django.utils import timezone
from datetime import timedelta
from .rag.pipeline import RAGPipeline
from .usage_tracker import record_usage

from .analytics import (
    get_current_rates,
    get_last_30_min_series,
    get_today_hourly_series,
    get_weekly_series,
)


def initialize_chat(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome! Ask Rithik is ready."
    })
    
def home(request):
    return render(request, "index.html")

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .rag.pipeline import RAGPipeline


pipeline = RAGPipeline()
@csrf_exempt
def chat(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Only POST request is allowed."
            },
            status=405
        )

    try:
        status = LLMStatus.objects.first()

        if status and not status.is_active:

            return JsonResponse(
                {
                    "response": status.message,
                    "chat": "blocked"
                },
                status=503
            )

        data = json.loads(request.body)

        question = data.get("message", "").strip()

        if not question:

            return JsonResponse(
                {
                    "error": "Message cannot be empty."
                },
                status=400
            )
        
        if not request.session.session_key:
            request.session.create()

        print("Session Key:", request.session.session_key)
        print("Cookie sessionid:", request.COOKIES.get("sessionid"))
        print("Request session_key:", request.session.session_key)
        SESSION_DURATION = timedelta(minutes=30)

        first_message_time = request.session.get("first_message_time")

        if first_message_time is None:

            request.session["first_message_time"] = timezone.now().isoformat()

        else:

            first_message_time = timezone.datetime.fromisoformat(first_message_time)

            if timezone.now() - first_message_time >= SESSION_DURATION:

                request.session.flush()

        MAX_CONVERSATIONS = 7

        conversation_count = request.session.get("conversation_count", 0)
        print("Conversation Count Before:", conversation_count)
        print("Session Key:", request.session.session_key)

        if conversation_count >= MAX_CONVERSATIONS:
            return JsonResponse(
                {
                    "response": "Conversation limit reached. Please try again later.",
                    "chat": "Limit reached"
                },
                status=503
            )

        # --- LLM call now returns (answer, usage_dict) ---
        answer, usage = pipeline.ask(question)

        # --- Log this request and auto-toggle is_active based on rolling limits ---
        updated_status = record_usage(usage, session_key=request.session.session_key)

        # print("Usage this call:", usage)
        # print("LLM still active:", updated_status.is_active)

        request.session["conversation_count"] = conversation_count + 1
        print("Conversation Count After:", request.session["conversation_count"])
        request.session.modified = True
        request.session.save()
        return JsonResponse(
            {
                "response": answer
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )



def analytics_dashboard_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized. Please log in."}, status=401)

    status, _ = LLMStatus.objects.get_or_create(id=1)
    
    return JsonResponse({
        "current": get_current_rates(),
        "last_30_min": get_last_30_min_series(),
        "today_hourly": get_today_hourly_series(),
        "week_daily": get_weekly_series(),
        "llm_status": {
            "is_active": status.is_active,
            "message": status.message
        }
    })



from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid request body."}, status=400)

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return JsonResponse({"status": "error", "message": "Username and password required."}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"status": "success", "message": "Logged in successfully."})

    return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)


def logout_view(request):
    logout(request)
    return JsonResponse({"status": "success", "message": "Logged out."})


def check_auth(request):
    return JsonResponse({
        "authenticated": request.user.is_authenticated,
        "username": request.user.username if request.user.is_authenticated else None
    }) 

def dashboard_page(request):
    return render(request, "dashboard.html")



from django.views.decorators.http import require_POST


@require_POST
def toggle_llm(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized. Please log in."}, status=401)

    status, _ = LLMStatus.objects.get_or_create(id=1)

    # Flip the switch
    status.is_active = not status.is_active

    if not status.is_active:
        status.message = "The assistant has been manually paused by an admin. Please check back soon."
    else:
        status.message = "Server is down. Please try again later."  # reset to default when re-enabled

    status.save()

    return JsonResponse({
        "is_active": status.is_active,
        "message": status.message
    })