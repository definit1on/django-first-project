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


def add_to_wishlist(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    user.product_wishlist.add(product)
    return HttpResponseRedirect(reverse('telemart:product-detail',
                                kwargs={'slug': product.slug}))


def remove_from_wishlist(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    user.product_wishlist.remove(product)
    return HttpResponseRedirect(reverse('telemart:product-detail',
                                        kwargs={'slug': product.slug}))


def add_comment(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data.get('text')
        new_comment = Comment(author=user, product=product,
                              text=text)
        new_comment.save()
    return HttpResponseRedirect(reverse('telemart:product-detail',
                                        kwargs={'slug': product.slug}))


def config(request):
    context = {
        'company_form': CompanyForm(),
        'product_form': ProductForm(),
    }
    return render(request, template_name='telemart/config.html',
                  context=context)

def add_new_company(request):
    form = CompanyForm(request.POST)
    if form.is_valid():
        new_company = form.save(commit=False)
        if 'icon' in request.FILES:
            new_company.portrait = request.FILES['icon']
        new_company.save()
    return HttpResponseRedirect(reverse('telemart:company-list'))


def add_new_product(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        new_product = form.save(commit=False)
        if 'picture' in request.FILES:
            new_product.picture = request.FILES['picture']
        if 'description' in request.FILES:
            new_product.description = request.FILES['description']
        slug = '-'.join(p.lower() for p in new_product.title.split()) \
               + f'-{new_product.power}'
        new_product.slug = ''.join(c for c in slug if c.isalpha() or c.isdigit() or c == '-')
        new_product.save()
        form.save_m2m()
    return HttpResponseRedirect(reverse('telemart:product-list'))


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.order_by('-power')
    serializer_class = MovieSerializer1



