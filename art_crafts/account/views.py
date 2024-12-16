from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse,reverse_lazy
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ProfileUpdateForm, PasswordUpdateForm
from .models import CustomUser
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef, Max
import json
from django.apps import apps

Arts = apps.get_model('artists', 'Arts')
Category = apps.get_model('artists', 'Category')
wishlist = apps.get_model('artists', 'wishlist')
Bid = apps.get_model('artists', 'Bid')

def get_cities(request, state_name):
    with open('account/indian_states_cities.json', 'r') as f:
        data = json.load(f)
    cities = data["states"].get(state_name, [])
    return JsonResponse({'cities': cities})
# Registration View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Make user active immediately; adjust as per need
            user.username = user.email
            user.set_password(form.cleaned_data["password"])
            if form.cleaned_data['usertype'] == 'artist':
                user.description = form.cleaned_data['description']
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usertype = form.cleaned_data['usertype']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome {user.name}')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Forgot Password View
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                # Send email
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_url}',
                    'from@example.com',  # Adjust sender email
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset email sent.')
                return redirect('login')
            else:
                messages.error(request, 'No user found with this email.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

# Password Reset Confirm View
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful. Please log in.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'password_reset_confirm.html')
    else:
        messages.error(request, 'Invalid or expired link.')
        return redirect('forgot_password')

def load_states():
    with open('account/indian_states_cities.json', 'r') as f:
        data = json.load(f)
    return [(state, state) for state in data["states"].keys()]

@login_required
def dashboard(request):
    fullname = request.user.name
    context = {
        'fullname': fullname
    }
    return render(request, 'dashboard.html',context)

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to a profile or dashboard page

    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form})

@login_required
def bidding(request):
    fullname = request.user.name
    bidding = Bid.objects.filter(user=request.user)
    context = {
        'bidding' : bidding,
    }
    return render(request, 'bidding.html',context)

@login_required
def order(request):
    latest_bids = Bid.objects.filter(
        art=OuterRef('pk')
    ).order_by('-created_at')
    fullname = request.user.name
    orders = Bid.objects.filter(user=request.user).annotate(
        latest_bid_amount=Subquery(latest_bids.values('bid_price')[:1]),
    )
    context = {
        'orders' : orders,
    }
    return render(request, 'order.html', context)

@login_required
def wishlists(request):
    fullname = request.user.name
    wishlists = wishlist.objects.filter(user=request.user).select_related('art')
    context = {
        'wishlists' : wishlists
    }
    return render(request, 'wishlist.html', context)
