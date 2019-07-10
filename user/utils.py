from django.core.cache import cache
from django.shortcuts import render


def login_required(func):
    def wrapper(*args, **kwargs):
        #调用函数之前
        print('---------->',*args,**kwargs)
        # 调用函数
        request = args[0]
        token = request.COOKIES.get('token_')
        user = cache.get(token)
        if user:
            request.user=user
        else:
            return render(request,'login.html')

        return func(*args,**kwargs)
    return wrapper
