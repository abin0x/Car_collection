from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from . import forms
from django.contrib import messages
from django.contrib.auth import login
from .models import Car, Brand, Order
from .forms import UserRegisterForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import  login ,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy


class HomeView(View):
    def get(self, request, brand_slug=None):
        brands = Brand.objects.all()
        cars = Car.objects.all()

        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            cars = cars.filter(brand=brand)

        return render(request, 'cars/home.html', {'brands': brands, 'cars': cars})
class CarDetailView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        comments = car.comments.all()
        comment_form = CommentForm()
        return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments, 'comment_form': comment_form})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.car = car
            comment.save()
        return redirect('car_detail', pk=car.pk)


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'cars/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'cars/register.html', {'form': form})
    
class ProfileView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'profile.html', {'orders': orders})

@method_decorator(login_required, name='dispatch')
class BuyCarView(View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        if car.quantity > 0:
            car.quantity -= 1
            car.save()
            Order.objects.create(user=request.user, car=car)
        return redirect('profile')

def user_logout(request):
    logout(request)
    return redirect('home')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': profile_form})

        
class UserLoginView(LoginView):
    template_name = 'cars/register.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'cars/profile.html', {'orders': orders})

    def post(self, request):
        logout(request)
        return redirect('login')
    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserRegisterForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = UserRegisterForm(instance=request.user)
    
    return render(request, 'cars/update_profile.html', {'form': profile_form})
