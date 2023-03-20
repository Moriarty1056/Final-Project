from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Team, File
from .forms import FileForm, TeamCreationForm
from django.contrib.auth.models import User


@login_required
def workhome(request):
    return render(request, 'workhome.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            return redirect('workhome')
    else:
        form = FileForm()
    return render(request, 'upload_file.html', {'form': form})


@login_required
def uploaded_files(request):
    user = request.user
    files = File.objects.filter(uploaded_by=user)
    return render(request, 'uploaded_files.html', {'files': files})


@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()
            form.save_m2m()  
            return redirect('team_list')
    else:
        form = TeamCreationForm()
    return render(request, 'create_team.html', {'form': form})


@login_required    
def team_detail(request):
    user=request.user
    teams=user.teams.all()
    return render(request,'team_detail.html', {'teams':teams})