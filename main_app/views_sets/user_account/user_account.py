from django.shortcuts import render
from main_app.models.model_picture.picture import Picture

def user_account_see(request):
    new_obj = Picture.objects.all()
    return render(request, 'user_account/user_account.html',{"new_obj":new_obj})