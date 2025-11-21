from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm as DjangoPasswordResetForm

from .models import User

class UserCreationForm(forms.ModelForm):
    """
    Formulario de registro personalizado que permite registrarse con email O teléfono
    """
    email = forms.EmailField(
        label='Email',
        required=False,
        help_text='Proporciona email o teléfono (al menos uno es requerido)',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'tu@email.com'
        })
    )
    phone = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False,
        help_text='Formato: +52XXXXXXXXXX o XXXXXXXXXX',
        widget=forms.TextInput(attrs={
            'autocomplete': 'tel',
            'placeholder': '+52XXXXXXXXXX'
        })
    )
    display_name = forms.CharField(
        label='Nombre completo o de Negocio',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'name',
            'placeholder': 'Tu nombre o del negocio'
        })
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': '••••••••'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'phone', 'display_name')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        
        # Normalizar campos vacíos a None
        if email == "":
            cleaned_data["email"] = None
        if phone == "":
            cleaned_data["phone"] = None
        
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        
        if not email and not phone:
            raise forms.ValidationError("Debes proporcionar un email o un número de teléfono.")
        
        return cleaned_data

    def clean_email(self):
        """Validar que el email no exista si se proporciona"""
        email = self.cleaned_data.get('email')
        # Si está vacío, retornar None
        if not email or email == "":
            return None
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
    
    def clean_phone(self):
        """Validar que el teléfono no exista si se proporciona"""
        phone = self.cleaned_data.get('phone')
        # Si está vacío, retornar None
        if not phone or phone == "":
            return None
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Este teléfono ya está registrado.")
        return phone

    def clean_password2(self):
        """Verificar que las dos contraseñas coincidan"""
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return p2

    def save(self, commit=True):
        """Guardar el usuario con la contraseña hasheada"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(DjangoPasswordResetForm):
    """
    Formulario personalizado para reset de contraseña que soporta
    tanto email como teléfono
    """
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'tu@email.com'
        })
    )

    def get_users(self, email):
        """Obtener usuarios que coincidan con el email"""
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        return (u for u in active_users if u.has_usable_password())

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see this user's password, "
        ),
    )

    class Meta:
        model = User
        fields = ('email',
                'phone',
                'password',
                'display_name',
                'public_slug',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                )

    def clean_password(self):
        # Keep the existing hash idk why
        return self.initial["password"]