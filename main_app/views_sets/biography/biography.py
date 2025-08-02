from django.shortcuts import render
from main_app.models.model_picture.picture import Picture

def biography(request):
    objects = Picture.objects.all()
    return render(request, 'pages_main_biography/biography.html', {"objects": objects})
    