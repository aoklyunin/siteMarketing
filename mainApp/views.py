# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from mainApp import auth
from mainApp.forms import ConsumerForm, CustomerForm
from mainApp.models import InfoText, Consumer, Customer

a = '''
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from mainApp.forms import LoginForm, AttemptForm, AddTaskForm, AddAttemptForm, MarkForm, FloatForm
from .models import Student, Task, AttemptComment, Mark


# состояние не принятой задачи
STATE_NOT_SENDED_TO_CHECKING = 0
# состояние не принятого офрмления
STATE_NOT_ACCEPTED = 1
# состояние принятого оформления
STATE_ACCEPTED = 2
# состояние защищённой задачи
STATE_MARKED = 3
# состояние отправленной на проверку задачи
STATE_SENDED_TO_CHECKING = 4


# добавление задания
def addTask(request):
    # если пользователь - администратор
    if request.user.is_staff:
        # если POST-запрос
        if request.method == "POST":
            # создаём форму на основе данных, полученных из POST-запроса
            form = AddTaskForm(request.POST)
            # если форма заполнена корректно
            if form.is_valid():
                # название задания
                task_name = form.cleaned_data['task_name']
                # дата публикации
                pub_date = form.cleaned_data['pub_date']
                # создаём объект задания
                t = Task.objects.create(task_name=task_name,
                                        pub_date=pub_date,
                                        )
                # сохраняем
                t.save()
                # выводим сообщение об удачном создании задании
                messages.success(request, "Задание добавлено")

        # данные для начального заполнения формы
        initial_data = {
            'task_name': '',
            'pub_date': datetime.date.today(),
            'ins_form': LoginForm()
        }
        # выводим страницу создания задания
        return render(request, "mainApp/addTask.html", {
            "task_form": AddTaskForm(initial=initial_data),
            "login_form": LoginForm(),
            "user": request.user
        })
    else:
        # перенаправляем на главную страницу
        return HttpResponseRedirect('/')


# личный кабинет студентов
def personal(request):
    # по пользователю получаем имя
    student = Student.objects.get(user=request.user)
    # список попыток, созданных текущем пользователем
    mark_list = Mark.objects.filter(student=student).order_by('task')
    # считаем сумму оценок
    sum = 0
    for mark in mark_list:
        sum += mark.m_value

    return render(request, "mainApp/personal.html", {
        'login_form': LoginForm(),
        'mark_list': mark_list,
        'sum': sum,
    })


# просмотр попытки по id
def mark_detail(request, mark_id):
    # ищем попытку с заданным id
    mark = Mark.objects.get(id=mark_id)
    # если пользователь хочет добавить комментарий
    if request.method == "POST":
        form = AttemptForm(request.POST)
        if form.is_valid():
            # текст комментария
            text = form.cleaned_data['text']
            # студент, написавший комментарий
            student = Student.objects.get(user=request.user)
            # создаём комментарий
            comment_object = AttemptComment.objects.create(isReaded=False, text=text, author=student)
            # сохраняем комментарий
            comment_object.save()
            mark.comment.add(comment_object)
    form = AttemptForm()

    return render(request, "mainApp/mark_detail.html", {
        "mark": mark,
        "text_form": form,
        "login_form": LoginForm(),
        "user": request.user,
    })


# отправить оценку на проверку
def markMakeNeedCheck(request, mark_id):
    # ищем попытку с заданным id
    mark = Mark.objects.get(id=mark_id)
    # студент, написавший комментарий
    student = Student.objects.get(user=request.user)
    if (mark.student == student) and ((mark.state == 0) or (mark.state == 1)):
        mark.state = 4
        mark.save()
    return HttpResponseRedirect('/personal/')

# список заданий требующих проверку оформления
def markNeedCheckList(request):
    if request.user.is_staff:
        mark_list = Mark.objects.order_by('-add_date').filter(state=4)
        template = 'mainApp/markNeedCheckList.html'
        context = {
            "mark_list": mark_list,
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

# оценить работу
def doMark(request, state_val, mark_id):
    print(state_val)
    if request.user.is_staff:
        print("staff")
        # ищем попытку с заданным id
        mark = Mark.objects.get(id=mark_id)
        if state_val == "1" or state_val == "2":
            mark.state = state_val
            mark.save()
            return HttpResponseRedirect('/mark/list/')
        if state_val == "3":
            print(request.POST)
            if request.method == "POST":
                form = FloatForm(request.POST)
                print(form)
                if form.is_valid():
                    # текст комментария
                    val = form.cleaned_data['val']
                    print(val)
                    mark.m_value = val
                    mark.state = state_val
                    mark.save()
            return HttpResponseRedirect('/mark/list_accepted/')

    return HttpResponseRedirect('/')

# список работ с принятым оформлением
def mark_list_accepted(request):
    if request.user.is_staff:
        mark_list = Mark.objects.order_by('-add_date').filter(state=2)
        template = 'mainApp/markAcceptedList.html'
        context = {
            "mark_list": mark_list,
            'form': FloatForm(initial={'val': '0.0'}),
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

# список работ с непринятым оформлением
def mark_list_not_accepted(request):
    if request.user.is_staff:
        mark_list = Mark.objects.order_by('-add_date').filter(state=1)
        template = 'mainApp/markNotAcceptedList.html'
        context = {
            "mark_list": mark_list,
            'form': FloatForm(initial={'val': '0.0'}),
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

# список оцененных работ
def mark_list_marked(request):
    if request.user.is_staff:
        mark_list = Mark.objects.order_by('student').filter(state=3)
        template = 'mainApp/markMarkedList.html'
        context = {
            "mark_list": mark_list,
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')
'''


def personal_main(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    flg = 0
    try:
        us = Consumer.objects.get(user=request.user)
        flg = 1
    except:
        try:
            us = Customer.objects.get(user=request.user)
            flg = 2
        except:
            HttpResponseRedirect('/')

    print(flg)
    if flg == 1:
        if request.method == 'POST':
            # строим форму на основе запроса
            form = ConsumerForm(request.POST)
            if form.is_valid():
                us.qiwi = form.cleaned_data['qiwi']
                us.save()
                u = us.user
                u.first_name = form.cleaned_data['name']
                u.last_name = form.cleaned_data['second_name']
                u.save()

        form = ConsumerForm(initial={'qiwi': us.qiwi, 'name': us.user.first_name, 'second_name': us.user.last_name})
        template = 'consumer/main.html'
    else:
        if request.method == 'POST':
            # строим форму на основе запроса
            form = CustomerForm(request.POST)

            if form.is_valid():
                print(form.cleaned_data)
                us.qiwi = form.cleaned_data['qiwi']
                us.companyName = form.cleaned_data['name']
                us.save()

        form = CustomerForm(initial={'name': us.companyName, 'qiwi': us.qiwi})
        template = 'customer/main.html'

    context = {
        "user": request.user,
        "u": us,
        "flg": flg,
        "form": form,
    }
    return render(request, template, context)


def personal_balance(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    flg = 0
    try:
        Consumer.objects.get(user=request.user)
        flg = 1
    except:
        try:
            Customer.objects.get(user=request.user)
            flg = 2
        except:
            HttpResponseRedirect('/')

    if flg == 1:
        template = 'consumer/main.html'
    else:
        template = 'customer/main.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)


def personal_marketing(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    flg = 0
    try:
        Consumer.objects.get(user=request.user)
        flg = 1
    except:
        try:
            Customer.objects.get(user=request.user)
            flg = 2
        except:
            HttpResponseRedirect('/')

    if flg == 1:
        template = 'consumer/main.html'
    else:
        template = 'customer/main.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)
