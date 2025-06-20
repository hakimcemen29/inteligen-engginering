from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Projek(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projek')
    nama = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

class Meaningful(models.Model):
    projek = models.ForeignKey('Projek', on_delete=models.CASCADE, related_name='meaningfuls')
    objectives = models.TextField()
    outcomes = models.TextField()
    indicator = models.TextField()
    properties = models.TextField()
    tanggal_mulai = models.DateField(null=True, blank=True)
    tanggal_akhir = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.tanggal_mulai and self.tanggal_akhir:
            if self.tanggal_akhir < self.tanggal_mulai:
                raise ValidationError("Tanggal selesai tidak boleh sebelum tanggal mulai.")

    def __str__(self):
        return self.objectives

class Experience(models.Model):
    projek = models.ForeignKey(Projek, on_delete=models.CASCADE, related_name='experiences')
    automate = models.TextField()
    prompt = models.TextField()
    annotate = models.TextField()
    organization = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Experience untuk {self.projek.nama}"

class Implementasi(models.Model):
    projek = models.ForeignKey(Projek, on_delete=models.CASCADE, related_name='implementasis')
    proses = models.TextField()
    teknologi = models.TextField()
    bangun = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Implementasi untuk {self.projek.nama}"

class Batasan(models.Model):
    projek = models.ForeignKey(Projek, on_delete=models.CASCADE, related_name='batasans')
    batasan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Batasan untuk {self.projek.nama}"

class Relasi(models.Model):
    projek = models.ForeignKey(Projek, on_delete=models.CASCADE, related_name='relasis')
    relasi = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Relasi untuk {self.projek.nama}"

class Perencanaan(models.Model):
    projek = models.ForeignKey(Projek, on_delete=models.CASCADE, related_name='perencanaans')
    deployment = models.CharField(max_length=255)
    pemeliharaan = models.CharField(max_length=255)
    operasi = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perencanaan untuk {self.projek.nama}"
