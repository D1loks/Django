from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import random


def hello(request):
    if 'username' not in request.COOKIES:
        response = render(request, 'hello.html')
        response.set_cookie('username', 'Guest')
        response.set_cookie('views', 0)
    else:
        views = int(request.COOKIES.get('views', 0)) + 1
        response = render(request, 'hello.html')
        response.set_cookie('views', views)
    rendered_template = render(request, 'hello.html', {
         'username': request.COOKIES.get('username'),
         'views': request.COOKIES.get('views'),
        'csrftoken': request.COOKIES.get('csrftoken'),
         'sessionid': request.COOKIES.get('sessionid')
     })
    response.content = rendered_template.content
    return response


def calculator(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST['num1'])
        num2 = float(request.POST['num2'])
        operation = request.POST['operation']

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                raise Http404("Page not found")
            else:
                result = num1 / num2

    return render(request, 'calculator.html', {'result': result})


def landing_page(request):
    return render(request, 'landing_page.html')


def guess_the_number(request):
    message = ''
    target_number = request.session.get('target_number')

    if request.method == 'POST':
        if 'min' in request.POST and 'max' in request.POST:
            min_number = int(request.POST['min'])
            max_number = int(request.POST['max'])
            target_number = random.randint(min_number, max_number)
            request.session['target_number'] = target_number
            message = f'Гру розпочато!'
        elif 'guess_num' in request.POST and target_number is not None:
            gs_number = int(request.POST['guess_num'])
            if gs_number < target_number:
                message = 'Загадане число більше!'
            elif gs_number > target_number:
                message = 'Загадане число менше!'
            else:
                message = 'Вітаємо! Ви вгадали число!'
                del request.session['target_number']
    return render(request, 'guess_the_number.html', {'message': message, 'number': target_number})
