from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Obuca, Odeca, SlikaOdece, Tip, SlikaObuce, Boja, VelicinaObuce, VelicinaOdece

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'input username', 'placeholder': 'Email'})) 
    first_name = forms.CharField(label='First Name', max_length="100", widget=forms.TextInput(attrs={'class': 'input username', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='last Name', max_length="100", widget=forms.TextInput(attrs={'class': 'input username', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'password1', 'password2'}

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input username'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['label'] = 'Username'

        self.fields['password1'].widget.attrs['class'] = 'input username'
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password1'].widget.attrs['label'] = 'Password'

        self.fields['password2'].widget.attrs['class'] = 'input username'
        self.fields['password2'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['label'] = 'Confirm Password'

class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'input username', 'placeholder': 'Email'})) 
    first_name = forms.CharField(label='First Name', max_length="100", widget=forms.TextInput(attrs={'class': 'input username', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='last Name', max_length="100", widget=forms.TextInput(attrs={'class': 'input username', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email'}

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input username'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['label'] = 'Username'

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form for changing a user's password.
    Inherits from Django's built-in PasswordChangeForm.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update({"class": "input"})
        self.fields["new_password1"].widget.attrs.update({"class": "input"})
        self.fields["new_password2"].widget.attrs.update({"class": "input"})

# Forma za Ubacivanje Obuce
        
class ObucaForm(forms.ModelForm):
    boja = forms.ModelMultipleChoiceField(queryset=Boja.objects.all(), widget=forms.CheckboxSelectMultiple)
    velicina = forms.ModelMultipleChoiceField(queryset=VelicinaObuce.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Obuca
        fields = ['naziv', 'sifra', 'cena', 'marka', 'stanje', 'opis', 'glavnaSlika']
        widgets = {
            'naziv': forms.TextInput(attrs={'class': 'input'}),
            'sifra': forms.TextInput(attrs={'class': 'input'}),
            'cena': forms.NumberInput(attrs={'class': 'input'}),
            'marka': forms.Select(attrs={'class': 'input'}),
            'stanje': forms.TextInput(attrs={'class': 'input'}),
            'opis': forms.Textarea(attrs={'class': 'input'}),
            'glavnaSlika': forms.ClearableFileInput(attrs={'class': 'input'}),
        }

class SlikaObuceForm(forms.ModelForm):
    class Meta:
        model = SlikaObuce
        fields = ['slika']
        widgets = {
            'slika': forms.ClearableFileInput(attrs={'class': 'input'}),
        }

ObucaFormSet = forms.inlineformset_factory(
    Obuca,
    SlikaObuce,
    form=SlikaObuceForm,
    extra=5,  # Maksimalno 5 slika može biti dodato
    can_delete=False,
)

# Forma za Ubacivanje Odece
        
class OdecaForm(forms.ModelForm):
    boja = forms.ModelMultipleChoiceField(queryset=Boja.objects.all(), widget=forms.CheckboxSelectMultiple)
    velicina = forms.ModelMultipleChoiceField(queryset=VelicinaOdece.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Odeca
        fields = ['naziv', 'sifra', 'tip', 'cena', 'marka', 'stanje', 'opis', 'glavnaSlika']
        widgets = {
            'naziv': forms.TextInput(attrs={'class': 'input'}),
            'sifra': forms.TextInput(attrs={'class': 'input'}),
            'tip': forms.Select(attrs={'class': 'input'}),
            'cena': forms.NumberInput(attrs={'class': 'input'}),
            'marka': forms.Select(attrs={'class': 'input'}),
            'stanje': forms.TextInput(attrs={'class': 'input'}),
            'opis': forms.Textarea(attrs={'class': 'input'}),
            'glavnaSlika': forms.ClearableFileInput(attrs={'class': 'input'}),
        }

class SlikaOdeceForm(forms.ModelForm):
    class Meta:
        model = SlikaOdece
        fields = ['slika']
        widgets = {
            'slika': forms.ClearableFileInput(attrs={'class': 'input'}),
        }

OdecaFormSet = forms.inlineformset_factory(
    Odeca,
    SlikaOdece,
    form=SlikaOdeceForm,
    extra=5,  # Maksimalno 5 slika može biti dodato
    can_delete=False,
)