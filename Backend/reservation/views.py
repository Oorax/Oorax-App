from .forms import *
from django.shortcuts import render, redirect,get_object_or_404



# page d'accueil
def matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        mat = request.POST["mat"]
        print(mat)
        if form.is_valid():
            user = form.save(commit=False)
            user.session_mat_id=mat
            user.save()
            session=Session.objects.all()
            return render(request, 'reservation/matiere_form.html', {'form': form,'session':session})
        else:
            redirect('matiere')
    else:
        form = MatiereForm()
        session = Session.objects.all()
    return render(request, 'reservation/matiere_form.html', {'form': form,'session':session})


def session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            return render(request, 'reservation/session_form.html', {'form': form})
        else:
            redirect('session')
    else:
        form = SessionForm()

    return render(request, 'reservation/session_form.html', {'form': form})

def reservation(request):
    session=Session.objects.all()
    return render(request, 'reservation/reservation_form.html',{'session':session})


def envoi_reserve(request,id):
    sess = Session.objects.get(id=id)
    s=sess.id
    user_id=request.user.id
    print(s,user_id)
    session = Session.objects.all()
    return render(request, 'reservation/reservation_form.html',{'session':session})

def user_eleve(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form = UserForm()
            return render(request, 'reservation/user_form.html', {'form': form})
        else:
            redirect('user_eleve')
    else:
        form = UserForm()

    return render(request, 'reservation/user_form.html',{'form':form})
