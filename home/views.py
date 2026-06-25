from django.shortcuts import render
import os

def home(request):
    """ A view to return home page """

    context = {
        "google_maps_api_key": os.environ["GOOGLE_MAPS_API_KEY"],
    }

    return render(request, "home/home.html", context)