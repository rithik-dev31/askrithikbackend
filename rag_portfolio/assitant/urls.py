from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("initialize/", views.initialize_chat, name="initialize"),
    path("chat/", views.chat, name="chat"),
    path("api/analytics/", views.analytics_dashboard_data, name="analytics_dashboard_data"),
    path("api/login/", views.login_view, name="login"),
    path("api/logout/", views.logout_view, name="logout"),
    path("api/check-auth/", views.check_auth, name="check_auth"),
    path("dashboard/", views.dashboard_page, name="dashboard"),
    path("api/toggle-llm/", views.toggle_llm, name="toggle_llm"),

]