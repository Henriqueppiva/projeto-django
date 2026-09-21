from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from .forms import RegistroForm
from .models import Aluno


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def register(request):
    if request.method != 'POST':
        form = RegistroForm()
    else:
        form = RegistroForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            Aluno.objects.create(usuario=new_user, nome=form.cleaned_data["nome"])
            authenticated_user = authenticate(
                username=new_user.username,
                password=request.POST.get('password1')
            )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('pricipal:aluno_index'))

    contexto = {
        'form': form,
    }

    return render(request, 'users/register.html', contexto)