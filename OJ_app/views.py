from argparse import FileType
from codeop import Compile
import compileall
import filecmp
import fileinput
from multiprocessing.pool import RUN
from django.shortcuts import get_object_or_404, redirect,render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import subprocess,os,sys
from django.contrib.auth.forms import UserCreationForm
import os.path
from .models import Problem,Testcase,Submission
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login as auth_login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
import subprocess
from datetime import datetime
import random
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


COMPILE = ["g++", "temp.cpp"]
RUN = ["./a.out"]


#@login_required(login_url='OJ_app:login')
def index(request):
    Problem_list = Problem.objects.order_by('problemid')
    context = {'Problem_list': Problem_list}
    return render(request, 'OJ_app/index.html', context)

@login_required(login_url='OJ_app:login')
def detail(request, problemid):
    problem = get_object_or_404(Problem, pk=problemid)
    return render(request, 'OJ_app/detail.html', {'problem': problem})

def login(request):
    if request.user.is_authenticated:
        return redirect('OJ_app:home')
    
    else:    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('OJ_app:index')

            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'OJ_app/login.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('OJ_app:home')
    
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('OJ_app:login')

        context = {'form':form}
        return render(request, 'OJ_app/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('OJ_app:login')

@login_required(login_url='OJ_app:login')
def leaderboard(request):
    recent_submissions = Submission.objects.all().order_by('-submissiontime')[:10]
    return render(request, 'OJ_app/leaderboard.html', {"result": recent_submissions})
   

    
def submit(request, problemid):
    code = request.POST['code']
    with open('temp.cpp', 'w') as file:
        file.write(code)
   

    _compile = subprocess.run(Compile)
    if (_compile.returncode != 0):
        verdict = Submission.Verdict.COMPILATION_ERROR
    else:
        tests = Testcase.objects.filter(problem__id = problemid)
        verdict = Submission.Verdict.Success
        for test in tests:
            input = test.input
            expected = test.output
            try:
                _run = subprocess.run(RUN, stdout=subprocess.PIPE, input=input, encoding='ascii', timeout=1, check=True)
                actual = _run.stdout
                if (expected != actual):
                    verdict = Submission.Verdict.Wrong_Output
                    break
                else:
                    verdict = Submission.Verdict.Success
            except subprocess.TimeoutExpired:
                verdict = Submission.Verdict.Time_Limit_Exceeded
                break
            except Exception as e:
                verdict = Submission.Verdict.Runtime_Error
                print(e)
                break

    sol = Submission(
        problem = Problem.objects.get(pk = problemid),
        verdict = verdict,
        submissiontime = datetime.now
    )
    sol.save()
    return redirect('leaderboard')

    

 
    
    


