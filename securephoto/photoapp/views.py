import base64
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import EncryptedPhoto

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_photo')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class UploadPhotoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        photo = request.FILES.get('photo')
        encrypted_photo = EncryptedPhoto.encrypt_photo(photo.read())
        return redirect('view_photo', pk=encrypted_photo.pk)

class ViewPhotoView(LoginRequiredMixin, View):
    def get(self, request, pk):
        photo = EncryptedPhoto.objects.get(pk=pk)
        decrypted_data = photo.decrypt_photo()
        decrypted_data_base64 = base64.b64encode(decrypted_data).decode('utf-8')
        return render(request, 'view.html', {'photo_data': decrypted_data_base64})
    
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(EncryptedPhoto, pk=pk)
    if request.method == 'POST':
        photo.delete()
        return redirect('upload_photo')
    return render(request, 'delete.html', {'photo': photo})

