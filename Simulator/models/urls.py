"""
URL configuration for Simulator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views.views import index, login, buy_order, sell_order, get_user_stats, check_for_bankruptcy,delete_user, signup, login_py, signup_py, fetch_orderbook, chart_py, questions_py, clear_pending_orders

# TODO: Add all necessary url patterns

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("",index, name="index"),
    path("login/", login, name="login"), 
    path("signup/", signup, name="signup"), 
    path("api/buy_order/", buy_order, name="buy_order"),
    path("api/sell_order/", sell_order, name="sell_order"),
    path("api/update_userstats", get_user_stats, name='update_userstats'),
    path("api/login_py", login_py, name='login_py'),
    path("api/signup_py", signup_py, name='signup_py'),
    path("api/fetch_orderbook", fetch_orderbook, name = "fetch_orderbook"),
    path("api/chart_py", chart_py, name='chart_py'),
    path("api/questions_py", questions_py, name='questions_py'),
    path("api/clear_pending_orders", clear_pending_orders, name = 'clear_pending_orders'),
    # These two haven't been implemented into the app.js yet
    path("api/check_for_bankruptcy", check_for_bankruptcy, name='check_for_bankruptcy'),
    path("api/delete_user", delete_user, name='delete_user')
]
