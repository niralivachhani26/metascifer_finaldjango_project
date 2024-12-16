from celery import shared_task
from django.utils.timezone import now
from django.apps import apps

Arts = apps.get_model('artists', 'Arts')
Bid = apps.get_model('artists', 'Bid')

@shared_task
def finalize_auction_winners():
    expired_auctions = Arts.objects.filter(auction_date_time__lt=now())

    for art in expired_auctions:
        highest_bid = Bid.objects.filter(art=art).latest('created_at')
        if highest_bid:
            highest_bid.status = 'win'
            highest_bid.save()
            notify_winner(highest_bid)

def notify_winner(highest_bid):
    if highest_bid.user:
        print(f"Winner for {highest_bid.art.title}: {highest_bid.user.name}")