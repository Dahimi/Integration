from time import time, sleep
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import *


@login_required(login_url="login")
def Solve_Problem(request, id):
    problem = Problem.objects.get(id=id)
    participant = get_participant(request)
    advancement, results = get_advancement(problem, participant)
    context = {"problem": problem, "advancement": advancement, "results": results}
    return render(request, "Problem.html", context)


@login_required(login_url="login")
def Home(request):
    # fill_problem(r"C:\Users\hamza.thaifa\Desktop\problems.xlsx")
    # fill_test(r"C:\Users\hamza.thaifa\Desktop\tests.xlsx")
    # fill_participant_user(r"C:\Users\hamza.thaifa\Desktop\Participants.xlsx")
    problems = Problem.objects.all()
    participant = get_participant(request)
    advancements = [get_percentage_color(problem, participant) for problem in problems]
    info = list(zip(problems, advancements))
    context = {"info": info, "participant": participant}
    return render(request, "Home.html", context)


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(
                request, "Le nom d'utilisateur ou le mot de passe est incorrect"
            )
    return render(request, "LoginPage.html")


def Logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def Ranking(request):
    participants = (
        Participant.objects.filter(~Q(Username="e-plusplus"))
        .order_by("Score")
        .reverse()
    )
    context = {"participants": participants, "pass": 3}
    return render(request, "Ranking.html", context)


@csrf_exempt
def Lunch_Tests(request, id):
    user_code = request.POST["code"]
    response, information = get_response(request, user_code, id)
    Update_Advancement(request, id, user_code, information)
    Update_Score(request)
    sleep(2)

    return HttpResponse(response)
