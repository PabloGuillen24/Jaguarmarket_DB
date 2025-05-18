from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Producto

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


CARRERAS_OPCIONES = [
    ('Ing. Sistemas', 'Ingeniería en Sistemas'),
    ('Ing. Industrial', 'Ingeniería Industrial'),
    ('Ing. Civil', 'Ingeniería Civil'),
    ('Administración', 'Administración'),
    ('Contaduría', 'Contaduría'),
    ('Arquitectura', 'Arquitectura'),
    # Puedes agregar más aquí
]

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model  = PerfilUsuario
        fields = ['telefono', 'foto']  # solo teléfono y foto
        widgets = {
            'telefono': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ej. 521234567890'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    # opcional: añadir clases bootstrap
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
