from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.contrib.auth import login
from django.db.models import Q


class MainPageView(View):

    def get(self, request):
        return render(request, 'home.html', context={
         })


class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', context={
            'form' : form
        })

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signup.html', context={
            'form' : form
        })


class SignInView(View):

    def get(self, request):
        form = SignInForm()
        return render(request, 'signin.html', context={
            'form' : form
        })

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'signin.html', context={
            'form' : form
        })