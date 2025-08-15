from django.shortcuts import render

from main_app.models.model_news.news import News


def comfidence(request):
    useda = News.objects.all()
    return render(request,'use_politics/Politicsconfidentions.html',{'useda':useda})