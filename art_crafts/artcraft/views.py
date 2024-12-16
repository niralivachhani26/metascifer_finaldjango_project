from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import Contact
from django.apps import apps
from django.db.models import Subquery, OuterRef, Max
from django.utils.timezone import now

CustomUser = apps.get_model('account', 'CustomUser')
Arts = apps.get_model('artists', 'Arts')
Category = apps.get_model('artists', 'Category')
wishlist = apps.get_model('artists', 'wishlist')
Bid = apps.get_model('artists', 'Bid')


def home(request):
  artist = CustomUser.objects.filter(usertype='artist')[:4]
  arts = Arts.objects.all()[:4]
  context = {
    'artist' : artist,
    'arts' : arts,
  }
  return render(request, 'home.html', context)

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      email = form.cleaned_data['email']
      subject = form.cleaned_data['subject']
      message = form.cleaned_data['message']

      form.save()


      messages.success(request, "Your message has been sent successfully!")  # Redirect to a success page
    else:
      print(form.errors)
  else:
    form = ContactForm()

  return render(request, 'contact.html', {'form': form})

def faq(request):
  return render(request, 'faq.html')

def about(request):
  return render(request, 'about.html')

def how_to_bid(request):
  return render(request, 'how_to_bid.html')

def how_to_sell(request):
  return render(request, 'how_to_sell.html')

def terms_condition(request):
  return render(request, 'terms_condition.html')

def privacy_policy(request):
  return render(request, 'privacy_policy.html')

def art_list(request, user_id):
  latest_bids = Bid.objects.filter(
    art=OuterRef('pk')
  ).order_by('-created_at')

  user = get_object_or_404(CustomUser, id=user_id)
  arts = Arts.objects.filter(user=user).annotate(
        latest_bid_amount=Subquery(latest_bids.values('bid_price')[:1]),
    )
  if request.user.is_authenticated:
      wishlists = wishlist.objects.filter(user=request.user).values_list('art_id', flat=True)
  else:
      wishlists = []
  context = {
    'arts' : arts,
    'user' : user,
    'category' : '',
    'wishlists': wishlists
  }
  return render(request, 'art_list.html', context)

def art_list1(request, category_id):
  latest_bids = Bid.objects.filter(
    art=OuterRef('pk')
  ).order_by('-created_at')

  category = get_object_or_404(Category, id=category_id)
  arts = Arts.objects.filter(category=category).annotate(
        latest_bid_amount=Subquery(latest_bids.values('bid_price')[:1]),
    )
  if request.user.is_authenticated:
    wishlists = wishlist.objects.filter(user=request.user).values_list('art_id', flat=True)
  else:
    wishlists =[]
  context = {
    'arts' : arts,
    'category' : category,
    'user' : '',
    'wishlists': wishlists
  }
  return render(request, 'art_list.html', context)

@login_required
def add_wishlist(request, art_id):
  art = get_object_or_404(Arts, id=art_id)
  user = request.user

  record = wishlist(art=art, user=user)
  record.save()

  return redirect('/account/wishlist')

def art_details(request, art_id):
  art = get_object_or_404(Arts, id=art_id)
  if request.user.is_authenticated:
    wishlists = wishlist.objects.filter(user=request.user , art= art).values_list('art_id', flat=True)
  else:
    wishlists =[]

  latest_bid = Bid.objects.filter(art=art).latest('created_at')
  if art.auction_date_time and art.auction_date_time > now():
      future_date = art.auction_date_time
  else:
      future_date = None
  context = {
    'art' : art,
    'future_date': future_date,
    'wishlists': wishlists,
    'latest_bid': latest_bid,
  }
  return render(request, 'art_details.html', context)


@login_required
def place_bid(request):
  if request.method == 'POST':
    art_id = request.POST.get('artid')
    art = get_object_or_404(Arts, id=art_id)
    user = request.user
    price = request.POST.get('quantity')

    record = Bid(art=art,user=user, bid_price=price)
    record.save()

    messages.success(request, "Your Bid Placed Successfully!")
    return redirect('/account/bidding')

  else:
    return redirect('/account/bidding')

def artist_detail(request, user_id):
  user = get_object_or_404(CustomUser, id=user_id)

  context = {
    'artist': user,
  }
  return render(request, 'artist_detail.html', context)





