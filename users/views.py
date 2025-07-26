from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import UserSerializer

# Create your views here.

@extend_schema(
    summary="Registrar usuario",
    description="Crea una nueva cuenta de usuario en el sistema",
    examples=[
        OpenApiExample(
            'Nuevo usuario',
            value={
                'username': 'usuario_nuevo',
                'email': 'usuario@ejemplo.com',
                'password': 'contraseña_segura123'
            }
        ),
    ],
    tags=['authentication']
)
class RegisterView(generics.CreateAPIView):
    """
    Vista para el registro de nuevos usuarios.
    
    Permite crear una nueva cuenta de usuario con username, email y password.
    La contraseña se encripta automáticamente antes de guardar en la base de datos.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
