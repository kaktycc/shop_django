from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
import django.contrib.auth as auth
from django.urls import reverse
import datetime
from mainapp.views import get_basket

# Create your views here.
def login(request):
    if 'next' in request.GET.keys():
        next = request.GET['next']
    else:
        next=''

    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST['password']
        print(username, passwd)

        user = auth.authenticate(username = username, password=passwd)
        if user:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    form = ShopUserLoginForm(data=request.POST or None)
    context = {
        'form' : form,
        'date_time': datetime.date.today,
        'next': next,
    }
    return render(request, 'authapp/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))

def register(request):
    title = 'Регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form,
        'date_time': datetime.date.today,
    }
    return render(request, 'authapp/register.html', context)

def edit(request):
    title = 'Редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'title': title,
        'edit_form': edit_form,
        'date_time': datetime.date.today,
        'basket': get_basket(request),
    }
    return render(request, 'authapp/edit.html', context)