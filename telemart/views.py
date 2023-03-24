from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

from .serializers import *
from .models import *
from .forms import *

def index(request):
    context = {
        'best_products': Product.objects.order_by('-power')[:4],
        'companies': Company.objects.order_by('-name')[:4],
        'gpus': Product.objects.filter(company__name='NVIDIA').order_by('-power')[:4],
        'cpus': Product.objects.filter(Q(company__name='AMD') | Q(company__name='Intel')).order_by('-power')[:2],
        'motherboards': Product.objects.filter(company__name='MSI').order_by('-power'),
        'memory': Product.objects.filter(company__name='HyperX'),
        'pus': Product.objects.filter(Q(company__name='Chieftec') | Q(company__name='Deepcool')),
    }
    return render(request, template_name='telemart/index.html',
                  context=context)


class CompanyListView(ListView):
    model = Company


class CompanyDetailView(DetailView):
    model = Company
    # login_url = reverse_lazy('imdb:login-page')


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all().order_by('-title')
    paginate_by = 12


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'comment_form': CommentForm(),
    }


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('telemart:index'))


def login_page(request):
    context = {}
    if 'next' in request.GET:
        context['next'] = request.GET['next']
    return render(request, template_name='telemart/login_page.html',
                  context=context)


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    next = request.POST.get('next')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect(reverse('telemart:index'))
    else:
        context = {'message': 'Incorrect username or password. Try again'}
        if next:
            context['next'] = next
        return render(request, template_name='telemart/login_page.html',
                      context=context)


def search(request):
    match = request.POST.get('match')
    if match:
        company_list = Company.objects.filter(name__icontains=match)
        product_list = Product.objects.filter(title__icontains=match)
        context = {
            'match': match,
            'company_list': company_list,
            'product_list': product_list,
        }
        return render(request, template_name='telemart/search.html',
                      context=context)
    else:
        return HttpResponseRedirect(reverse('telemart:index'))






