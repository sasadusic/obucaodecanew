from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UpdateProfileForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from .forms import ObucaForm, ObucaFormSet, OdecaForm, OdecaFormSet
from .models import Obuca, Odeca, SlikaObuce, SlikaOdece, Boja, VelicinaObuce, NacinKupovine, Praćenje
from django.db import transaction
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Wellcome {username.title()}, you are logged in')
            return redirect('index')
        else:
            messages.success(request, f'Wrong username or password please try again')
            return redirect('index')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout_user(request):
    messages.success(request, f'You are logged out, Login to continue')
    logout(request)
    
    return redirect('index')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Wellcome {username.title()}, you are registered')
            return redirect('index')

    else:
        form = SignUpForm()

        return render(request, 'register.html', {'form': form})
        
    return render(request, 'register.html', {'form': form})

@login_required(login_url="login")
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url="login")
def  update_profile(request):
    current_user = request.user
    if request.method=='POST':
        form = UpdateProfileForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated successfully!")
            return redirect("profile")
        else:
            messages.error(request,"Please correct the error below.")
    else:
        form = UpdateProfileForm(instance=current_user)
    
    context={"form":form}
    return render(request,'update_profile.html',context)    

@login_required(login_url="login")
def change_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=current_user, data=request.POST)
        if form.is_valid():
            form.save()
            # Logout the user first to get rid of session cookie
            logout(request)
            messages.warning(request, "Password changed successfully! Please login again.")
            return redirect('logout')
        else:
            messages.error(request, "Error in password reset. Please try again.")
            
    else:
        form = CustomPasswordChangeForm(user=current_user)
        
    return render(request, 'change_password.html', {'form': form})

User = get_user_model()

@login_required(login_url="login")
def delete_profile(request):
    """
    View function for deleting a user's profile.
    Only accessible to authenticated users.
    """
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.delete()
        return redirect("index")
    
def kreiraj_obucu(request):
    if request.method == 'POST':
        form = ObucaForm(request.POST, request.FILES)
        formset = ObucaFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                obuca = form.save()
                formset.instance = obuca
                formset.save()
                # Sačuvajte boje povezane sa obućom
                obuca.boja.set(form.cleaned_data['boja'])
                # Sačuvajte veličine povezane sa obućom
                obuca.velicina.set(form.cleaned_data['velicina'])
            messages.success(request, 'Obuća je uspešno dodata.')
            return redirect('sva_obuca')
        else:
            messages.error(request, 'Došlo je do greške. Molimo pokušajte ponovo.')
    else:
        form = ObucaForm()
        formset = ObucaFormSet()
    return render(request, 'kreiraj_obucu.html', {'form': form, 'formset': formset})


def sva_obuca(request):
    query = request.GET.get('q')
    if query:
        obuca = Obuca.objects.filter(Q(naziv__icontains=query))
    else:
        obuca = Obuca.objects.all()
    return render(request, 'sva_obuca.html', {'obuca': obuca})


def detalji_obuce(request, pk):
    obuca = Obuca.objects.get(pk=pk)
    prati_obuca = obuca.praćenje_set.filter(korisnik=request.user).exists() if request.user.is_authenticated else False
    slike = SlikaObuce.objects.filter(obuca=obuca)
    nacin = NacinKupovine.objects.get(naziv='Za-obucu')
    return render(request, 'detalji_obuce.html', {'obuca': obuca, 'slike':  slike, 'nacin': nacin, 'prati_obuca': prati_obuca})

def obrisi_obucu(request, pk):
    obuca = Obuca.objects.get(pk=pk)
    slike = SlikaObuce.objects.filter(obuca=obuca)
    obuca.delete()
    slike.delete()
    return redirect('sva_obuca')

def kreiraj_odecu(request):
    if request.method == 'POST':
        form = OdecaForm(request.POST, request.FILES)
        formset = OdecaFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                odeca = form.save()
                formset.instance = odeca
                formset.save()
                # Sačuvajte boje povezane sa obućom
                odeca.boja.set(form.cleaned_data['boja'])
                # Sačuvajte veličine povezane sa obućom
                odeca.velicina.set(form.cleaned_data['velicina'])
            messages.success(request, 'Odeća je uspešno dodata.')
            return redirect('sva_odeca')
        else:
            messages.error(request, 'Došlo je do greške. Molimo pokušajte ponovo.')
    else:
        form = OdecaForm()
        formset = OdecaFormSet()
    return render(request, 'kreiraj_odecu.html', {'form': form, 'formset': formset})

def sva_odeca(request):
    query = request.GET.get('q')
    if query:
        odeca = Odeca.objects.filter(Q(naziv__icontains=query))
    else:
        odeca = Odeca.objects.all()
    return render(request, 'sva_odeca.html', {'odeca': odeca})

def detalji_odece(request, pk):
    odeca = Odeca.objects.get(pk=pk)
    slike = SlikaOdece.objects.filter(odeca=odeca)
    nacin = NacinKupovine.objects.get(naziv='Za-obucu')
    return render(request, 'detalji_odece.html', {'odeca': odeca, 'slike':  slike, 'nacin': nacin})

def obrisi_odecu(request, pk):
    odeca = Odeca.objects.get(pk=pk)
    slike = SlikaOdece.objects.filter(odeca=odeca)
    odeca.delete()
    slike.delete()
    return redirect('sva_odeca')

@login_required(login_url='login_user')
def prati_obucu(request, pk):
    obuca = get_object_or_404(Obuca, pk=pk)
    obuca.prati(request.user)
    return redirect('detalji_obuce', pk=pk)

@login_required(login_url='login_user')
def odprati_obucu(request, pk):
    obuca = get_object_or_404(Obuca, pk=pk)
    obuca.odprati(request.user)
    return redirect('detalji_obuce', pk=pk)

@login_required(login_url='login_user')
def korpa(request):
    obuca = request.user.praćenje_set.all()
    # obuca_ids = Praćenje.objects.filter(korisnik=request.user, prati=True, obuca__isnull=False).values_list('obuca', flat=True)
    # obuca = Obuca.objects.filter(id__in=obuca_ids)
    for o in obuca:
        print(o.obuca.cena)
    return  render(request, 'korpa.html', {'obuca': obuca})

lorem = 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, dolorum? Quam sed earum nostrum, amet fuga vel quod pariatur accusamus.'