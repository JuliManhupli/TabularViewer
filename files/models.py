from django.db import models


class UploadedFile(models.Model):
    name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
