from plyer import notification
import requests
import time
api_key = "da22f2fcab22170906aafd1e4f6fef9a"
city = "kampala"


def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5  # the notification will be visible for 5 seconds
    )

def send_wake_up_notification():
    send_notification('Good Morning!', 'Time to wake up!')

def send_prayer_reminder():
    send_notification('Prayer Reminder', 'Time to pray.')

def get_weather_update(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    # Check if the response contains the 'main' key
    if 'main' in weather_data:
        temp = weather_data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        description = weather_data['weather'][0]['description']
        return temp, description
    else:
        # Handle error: print the API response to debug
        print(f"Error fetching weather data: {weather_data}")
        return None, None

def send_weather_update(api_key, lat, lon):
    temp, description = get_weather_update(api_key, lat, lon)
    if temp is not None and description is not None:
        message = f"The current temperature is {temp:.2f}°C with {description}."
        send_notification('Weather Update', message)
    else:
        send_notification('Weather Update', 'Unable to fetch weather data.')

def automated_morning_routine():
    send_wake_up_notification()
    time.sleep(2)
    send_prayer_reminder()
    time.sleep(2)
    # Use the provided latitude and longitude values
    send_weather_update(f'{api_key}', 0.354875, 32.751628)

# Call the function to run the automated morning routine
automated_morning_routine()
