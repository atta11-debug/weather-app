from django.shortcuts import render
import requests
import datetime
from django.contrib import messages
from django.conf import settings


def home(request):
    city = request.POST.get("city", "Jhang")

    # Weather API
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "q": city,
        "appid": settings.WEATHER_API_KEY,
        "units": "metric"
    }

    # Default values
    description = icon = temp = "N/A"
    exception_occurred = False
    image_url = None  # Background image

    try:
        # 🌤 Fetch weather
        weather_response = requests.get(weather_url, params=weather_params)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            description = weather_data["weather"][0]["description"]
            icon = weather_data["weather"][0]["icon"]
            temp = weather_data["main"]["temp"]
        else:
            exception_occurred = True
            messages.error(request, "City not found.")

        # 🖼 Fetch city image from Unsplash API
        unsplash_url = f"https://api.unsplash.com/photos/random?query={city}&client_id={settings.UNSPLASH_API_KEY}"
        image_response = requests.get(unsplash_url)
        if image_response.status_code == 200:
            image_data = image_response.json()
            image_url = image_data["urls"]["regular"]  # You can also use "full" or "raw"
        else:
            # fallback image if Unsplash fails
            image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600"

    except requests.exceptions.RequestException:
        exception_occurred = True
        messages.error(request, "Network error. Please try again.")
        # fallback image
        image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600"

    day = datetime.date.today()
    print("Background image URL:", image_url)

    return render(
        request,
        "index.html",
        {
            "description": description,
            "icon": icon,
            "temp": temp,
            "day": day,
            "city": city,
            "exception_occurred": exception_occurred,
            "image_url": image_url,
        },
    )
