from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm

User = get_user_model()

class RegisterForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ['email','username','password1','password2']
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)