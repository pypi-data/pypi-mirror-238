import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST


# Create your views here.

@require_POST
def login_(request):
    data = json.loads(request.body.decode('utf-8'))
    user = authenticate(**data['formInline'])
    if user:
        login(request, user)
    else:
        return HttpResponseBadRequest('登录失败,输入信息错误')
    return HttpResponse('登录成功，即将进入系统')


@require_POST
def logout_(request):
    logout(request)
    return HttpResponse('成功退出登录')


@login_required(login_url='admin:login')
def workplace(request):
    return render(request, 'admin/workplace.html', {})


def console(request):
    return render(request, 'admin/console.html', {})


def custom_404(request):
    return render(request, 'admin/exception/404.html')


def custom_404_view(request, exception):
    return render(request, 'admin/exception/404.html')


def custom_403(request):
    return render(request, 'admin/exception/403.html')


def custom_403_view(request, exception):
    return render(request, 'admin/exception/403.html')


def custom_500(request):
    return render(request, 'admin/exception/500.html')


def custom_500_view(request):
    return render(request, 'admin/exception/500.html')


def success(request):
    return render(request, 'admin/result/success.html')


def info(request):
    return render(request, 'admin/result/info.html')


def basic(request):
    return render(request, 'admin/comp/form/basic.html')


def fail(request):
    return render(request, 'admin/result/fail.html')


def account(request):
    return render(request, 'admin/setting/account/account.html')


def system(request):
    return render(request, 'admin/setting/system/system.html')



