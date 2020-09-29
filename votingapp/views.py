from django.shortcuts import render,redirect
from votingapp.forms import UserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
from votingapp.forms import *
# Create your views here.
def home(request):
    user = request.user
    if user.is_authenticated:
        username = user.username.title()
        return render(request,"votingapp/home.html",context={"username":username})
    return render(request,"votingapp/home.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect('votingapp:home')


@login_required(login_url="/voting/login")
def vote(request):
    user=request.user
    u=User.objects.get(username=user)
    if request.method=='POST':
        c_name=request.POST['name']
        c=Candidate.objects.get(name=c_name)
        v=c.no_votes+1
        c=Candidate.objects.filter(name=c_name).update(no_votes=v)
        c=VoterDetails.objects.filter(user=u).update(voted=True)
        return render(request,"votingapp/vote.html",context={'username':user})
    else:
        v=VoterDetails.objects.all()
        candidates=Candidate.objects.filter(Constituency=v.Constituency)
    return render(request,"votingapp/vote.html",context={'candidates':candidates,"vote_status":v.voted})
   
def register(request):
    registered=False
    if request.method=="POST":
        userform=UserForm(request.POST)
        conform=VoterForm(request.POST)
        if userform.is_valid() and conform.is_valid():
            user=userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()
            profile=conform.save(commit=False)
            profile.user=user
            profile.save()
            registered=True
    userform=UserForm(request.POST)
    conform=VoterForm(request.POST)
    return render(request,"votingapp/register.html",context={'registered':registered,'userform':userform,'conform':conform})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('votingapp:home')
        else:
            return redirect('votingapp:register')
    return render(request,"votingapp/login.html")