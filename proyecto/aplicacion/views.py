from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_staff = True 
            usuario.save()
            return redirect('/admin/') 
    else:
        form = UserCreationForm()
    
    return render(request, 'registro.html', {'form': form})