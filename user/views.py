import logging
import uuid
from time import sleep

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from user.forms import RegisterForm, LoginForm
from user.models import User
from user.task import sendmail
from user.utils import login_required


@cache_page(60 * 15)  # 缓存15分钟
def index(request):
    lists = []
    for i in range(10):
        lists.append("----》新闻%s" % i)
        sleep(0.5)
    return render(request, 'index.html', context={'lists': lists})


def search_keys(request):
    result = cache.keys("*")
    print('---result:', result)
    return HttpResponse('test')


def user_register(request):
    if request.method == 'GET':
        rform = RegisterForm()
        return render(request, 'register.html', context={'form': rform})
    else:
        rform = RegisterForm(request.POST)
        if rform.is_valid():
            data = rform.cleaned_data
            username = data.get('username')
            password = data.get('password')
            repassword = data.get('repassword')
            email = data.get('email')
            if password == repassword:
                password = make_password(password)
                user = User.objects.create(username=username, password=password)
                if user:
                    # 发送激活邮件
                    uid = str(uuid.uuid4()).replace('-', '')
                    cache.set(uid, user)
                    print('uid:', uid)
                    # 此时启动异步发送邮件
                    result = sendmail.delay(uid, email)

                    return HttpResponse('用户注册成功,赶快去激活吧！')
            return render(request, 'register.html', context={'form': rform, 'msg': '注册失败，重写注册'})


def user_login(request):
    if request.method == 'GET':
        lform = LoginForm()
        return render(request, 'login.html', context={'form': lform})
    else:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            data = lform.cleaned_data
            user = User.objects.filter(username=data.get('username')).first()
            if user and user.is_active:
                flag = check_password(data.get('password'), user.password)
                if flag:
                    # token 令牌
                    uid = uuid.uuid4()
                    token = str(uid).replace('-', '')
                    print("++++++++>token :", token)
                    cache.set(token, user, timeout=60 * 30)

                    # 创建response对象
                    res = HttpResponse('用户登录成功')
                    res.set_cookie('token_', token)
                    return res
            else:
                return render(request, 'login.html', context={'form': lform, 'msg': '请检查用户名或者用户没有激活！'})
        return render(request, 'login.html', context={'form': lform, 'msg': '用户名或者密码有误！'})


# 验证用户登录
@login_required
def add_cart(request):
    print("++++++++>", request.user)
    return HttpResponse('add_cart----->testing')


# 用户激活
def user_active(request, uid):
    user = cache.get(uid)
    user.is_active = True
    user.save()
    return HttpResponse('激活成功，赶快登陆吧！')


# 日志测试路由
def log_test(request):
    uid = request.GET.get('id')
    logger = logging.getLogger('user')
    try:
        user = User.objects.get(pk=uid)
        logger.info('获取用户:%s成功！'% user.username)
    except:
        logger.error('获取用户失败！')

    return HttpResponse('test --- log')


