from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from main_app.forms.account.user_account import PhoneNumberForm, EditProfileForm, CustomPasswordChangeForm

def add_phone(request):
    user = request.user
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account')  # имя страницы профиля
    else:
        form = PhoneNumberForm(instance=user)
    return render(request, 'account/add_phone.html', {'form': form})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'account/edit_profile.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Чтобы не разлогинило
            return redirect('account')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})
