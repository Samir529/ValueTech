from django.shortcuts import render
from datetime import date
from offers.models import Offer

def offers_list(request):
    today = date.today()
    # offers = Offer.objects.filter(end_date__gte=today).order_by("created_at")
    offers = Offer.objects.all().order_by("created_at")
    return render(request, "offers/offers.html", {"offers": offers})
