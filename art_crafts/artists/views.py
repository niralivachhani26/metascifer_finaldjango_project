from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm,ArtsForm
from django.apps import apps
from django.urls import reverse,reverse_lazy
from django.http import JsonResponse
from .models import Arts, Bid
from django.db.models import Subquery, OuterRef, Max
import json

CustomUser = apps.get_model('account', 'CustomUser')


@login_required
def dashboard(request):
    fullname = request.user.name
    context = {
        'fullname': fullname
    }
    return render(request, 'artist_dashboard.html',context)

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

    return render(request, 'artist_profile.html', {'form': form})

@login_required
def bidding(request):
    fullname = request.user.name
    user_arts = Arts.objects.filter(user=request.user)
    bidding = Bid.objects.filter(art__in=user_arts).select_related('art', 'user')
    context = {
        'bidding' : bidding
    }
    return render(request, 'bidding_list.html',context)

@login_required
def order(request):
    latest_bids = Bid.objects.filter(
        art=OuterRef('pk'),
        status = "win"
    ).order_by('-created_at')
    fullname = request.user.name
    user_arts = Arts.objects.filter(user=request.user)
    orders = Bid.objects.filter(art__in=user_arts, status='win').select_related('art', 'user')
    context = {
        'orders' : orders,
    }
    return render(request, 'order_list.html', context)

@login_required
def arts(request):
    fullname = request.user.name
    arts = Arts.objects.filter(user=request.user)
    context = {
        'arts' : arts
    }
    return render(request, 'arts.html', context)

@login_required
def add_arts(request):
    if request.method == "POST":
        form = ArtsForm(request.POST,request.FILES)
        if form.is_valid():
            art = form.save(commit=False)  # Don't save to the database yet
            art.user = request.user  # Assign the current user
            art.save()
            messages.success(request, 'Arts added successfully!')
        return redirect('arts')  # Replace with your desired redirect URL
    else:
        form = ArtsForm()
    return render(request, 'add_arts.html', {'form': form})

@login_required
def edit_arts(request, pk):
    art = get_object_or_404(Arts, pk=pk, user=request.user)
    if request.method == "POST":
        form = ArtsForm(request.POST,request.FILES, instance=art)
        if form.is_valid():
            art = form.save(commit=False)  # Don't save to the database yet
            art.save()
            messages.success(request, 'Arts updated successfully!')
        return redirect('arts')  # Replace with your desired redirect URL
    else:
        form = ArtsForm(instance=art)
    return render(request, 'edit_arts.html', {'form': form, 'art':art})

@login_required
def delete_arts(request, pk):
    art = get_object_or_404(Arts, pk=pk, user=request.user)
    art.delete()
    messages.success(request, 'Art delete successfully!')
    return redirect('arts')
# Create your views here.
