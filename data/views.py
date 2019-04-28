from django.shortcuts import render
from .models import ExtraInfo, States, Sprint, Achieve
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def test(request):
    user = request.user
    extra = ExtraInfo.objects.create(achieves=1, user=user)
    extra.save()
    return HttpResponse("Text only, please.", content_type="text/plain")


@login_required(login_url='/admin/')
def index(request):
    return render(request, 'index.html', {})


def current_sprint(request):
    current_sprint = Sprint.objects.all().order_by('-id')[0]
    current_states = States.objects.get(sprint=current_sprint, user=request.user)
    return render(request, 'current_kpi.html', {'current_states': current_states})


def logout_view(request):
    logout(request)
    return redirect('/')


def all_sprints_states(request):
    return render(request, 'all_sprints_states.html')


def all_sprints_state(request, state):
    states = States.objects.filter(user=request.user)
    all_states = []
    all_dates_start = []
    all_dates_end = []
    if state == 'per_from_all_tests':
        for state in states:
            all_states.append(state.per_from_all_tests)
            all_dates_start.append(state.sprint.date_start)
            all_dates_end.append(state.sprint.date_end)
    elif state == 'per_from_builds':
        for state in states:
            all_states.append(state.per_from_builds)
            all_dates_start.append(state.sprint.date_start)
            all_dates_end.append(state.sprint.date_end)
    elif state == 'num_commits':
        for state in states:
            all_states.append(state.num_commits)
            all_dates_start.append(state.sprint.date_start)
            all_dates_end.append(state.sprint.date_end)
    elif state == 'per_over_tests':
        for state in states:
            all_states.append(state.per_over_tests)
            all_dates_start.append(state.sprint.date_start)
            all_dates_end.append(state.sprint.date_end)
    else:
        for state in states:
            all_states.append(state.num_of_unclosed_tasks)
            all_dates_start.append(state.sprint.date_start)
            all_dates_end.append(state.sprint.date_end)
    return render(request, 'sprints_states.html', {'all_states': all_states, 'type': state, 'all_dates_start': all_dates_start, 'all_dates_end': all_dates_end})


def zones_of_growth(request):
    return render(request, 'zones_of_groth.html', {'role': request.user.extrainfo.role})


def achieves_states(request):
    achieves = Achieve.objects.filter(user=request.user)
    ach = [0, 0, 0, 0, 0]
    for achieve in achieves:
        if achieve.type_of_ach == 'PAL':
            print('PAL')
            ach[0] += 1
        elif achieve.type_of_ach == 'PFB':
            print('PFB')
            ach[1] += 1
        elif achieve.type_of_ach == 'NC':
            print('NC')
            ach[2] += 1
        elif achieve.type_of_ach == 'POT':
            print('POT')
            ach[3] += 1
        elif achieve.type_of_ach == 'NOUT':
            print('NOUT')
            ach[4] += 1

    return render(request, 'states_ahieves.html', {'ach': ach, 'length': len(Sprint.objects.all())})


def achieves_shop(request):
    return render(request, 'achieve_shop.html', {'balance': request.user.extrainfo.achieves})


def buy(request, achieve_name):
    if achieve_name == 'work':
        if request.user.extrainfo.achieves > 0:
            request.user.extrainfo.achieves -= 1
            request.user.extrainfo.bought += 'work '
    elif achieve_name == 'money':
        if request.user.extrainfo.achieves > 0:
            request.user.extrainfo.achieves -= 1
            request.user.extrainfo.bought += 'money '
    elif achieve_name == 'less':
        if request.user.extrainfo.achieves > 0:
            request.user.extrainfo.achieves -= 1
            request.user.extrainfo.bought += 'less '
    elif achieve_name == 'card':
        if request.user.extrainfo.achieves > 0:
            request.user.extrainfo.achieves -= 1
            request.user.extrainfo.bought += 'card '
    elif achieve_name == 'taxi':
        if request.user.extrainfo.achieves > 1:
            request.user.extrainfo.achieves -= 2
            request.user.extrainfo.bought += 'taxi '
    elif achieve_name == 'walk':
        if request.user.extrainfo.achieves > 1:
            request.user.extrainfo.achieves -= 2
            request.user.extrainfo.bought += 'walk '
    request.user.save()
    return redirect('/achieves/shop/')





