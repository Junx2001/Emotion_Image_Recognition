from django import forms
from .models import UploadedFile
from multiupload.fields import MultiFileField

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class UploadImagesForm(forms.Form):
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)  # Limit to 10 files, max 5MB each