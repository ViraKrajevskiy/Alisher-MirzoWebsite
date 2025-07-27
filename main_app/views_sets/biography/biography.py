from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from main_app.models.model_picture.picture import Picture


def biography(request):
    objects = Picture.objects.all()
    return render(request, 'pages_main_biography/biography.html', {"objects": objects})
    