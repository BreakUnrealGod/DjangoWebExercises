# from djangoday10.celery import app
#
#
# @app.task
# def add(x, y):
#     return x + y
#
#
# @app.task
# def mul(x, y):
#     return x * y
# 任务：耗时任务   发送邮件
from celery import shared_task
from django.core.mail import send_mail

from djangoday10.settings import EMAIL_HOST_USER


@shared_task
def sendmail(uid, email):
    print(uid,email)
    subject = '异步发送邮件测试'
    message = "亲爱的用户你好！点击激活用户<a href='http://127.0.0.1:8000/active/%s'> 激活 </a>" % uid
    print('----->1')
    send_mail(subject, message='', from_email=EMAIL_HOST_USER, recipient_list=[email,], html_message=message)
