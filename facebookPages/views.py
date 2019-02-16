from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

def HomePage(request):
    url = reverse("login")
    if request.user.is_authenticated:
        url = reverse("dashboard")
    return redirect(url, args=(),kwargs={})