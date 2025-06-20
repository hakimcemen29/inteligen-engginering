from rest_framework import serializers
from .models import Projek

class ProjekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projek
        fields = ['id', 'nama', 'user']  # pastikan 'user' masuk kalau butuh untuk Android
