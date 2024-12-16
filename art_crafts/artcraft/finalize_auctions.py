from django.core import checks
from django.core.management.base import BaseCommand
from django_cron import CronJobBase, Schedule
from django.utils.timezone import now
from django.apps import apps

CustomUser = apps.get_model('account', 'CustomUser')
Arts = apps.get_model('artists', 'Arts')
Category = apps.get_model('artists', 'Category')
wishlist = apps.get_model('artists', 'wishlist')
Bid = apps.get_model('artists', 'Bid')

class Command(BaseCommand):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'artcraft.finalize_auctions'

    def do(self):
        expired_auctions = Arts.objects.filter(auction_date_time__lte=now())
        for auction in expired_auctions:
            highest_bid = auction.bids.order_by('-bid_price').first()
            if highest_bid:
                highest_bid.status = 'win'
                highest_bid.save()

                self.stdout.write(f"Winner Finalized for auction '{ auction.title }':{ highest_bid.user.name }")
            else:
                self.stdout.write(f"No Bids for auction '{auction.title}'")