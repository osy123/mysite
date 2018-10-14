from django.http import HttpResponseRedirect
from django.shortcuts import render
from guestbook import models

# Create your views here.
def index(request):
    results = models.fetchall()

    count = len(results)
    for result in results:
        result['number'] = count
        count -= 1

    data = {"guestbook_list":results}

    return render(request, 'guestbook/index.html', data)


def deleteform(request):
    no = request.GET['no']
    data = {"no":no}
    return render(request, 'guestbook/deleteform.html', data)


def add(request):
    name = request.POST['name']
    password = request.POST['password']
    message = request.POST['message']

    models.insert((name, password, message))

    return HttpResponseRedirect("/guestbook")


def delete(request):
    no = request.POST['no']
    password = request.POST['password']
    data = {"no":no, "password":password}

    models.delete((no, password))

    return HttpResponseRedirect("/guestbook", data)

