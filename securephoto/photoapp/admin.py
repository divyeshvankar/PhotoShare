from django.contrib import admin
from .models import EncryptedPhoto

class EncryptedPhotoAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(EncryptedPhoto, EncryptedPhotoAdmin)
