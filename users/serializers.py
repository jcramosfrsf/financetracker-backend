from django.contrib.auth.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Usuario de ejemplo',
            value={
                'id': 1,
                'username': 'usuario_ejemplo',
                'email': 'usuario@ejemplo.com',
                'password': 'contraseña_segura123'
            }
        )
    ]
)
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User.
    
    Permite crear nuevos usuarios con encriptación automática de contraseñas.
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        read_only_fields = ('id',) 