import requests
import streamlit as st
import json

# SkyScanner API URL
url = "https://sky-scanner3.p.rapidapi.com/flights/search-multi-city"

# Headers for API authentication
headers = {
    'x-rapidapi-key': "2a44a82b8cmsh488f974a35b410dp1ee6b4jsn541b54c4cb0a",
    'x-rapidapi-host': "sky-scanner3.p.rapidapi.com",
    'Content-Type': "application/json"
}

# Modify the payload based on user input
payload = {
    "market": "US",
    "locale": "en-US",
    "currency": "USD",
    "adults": 1,
    "children": 0,
    "infants": 0,
    "cabinClass": "business",
    "stops": ["direct"],
    "sort": "cheapest_first",
    "flights": [{
        "fromEntityId": "LHR",  # London Heathrow (Hardcoded, or you can replace it with user input)
        "toEntityId": "JFK",  # User input for destination
        "departDate": "2024-12-17"  # User input for departure date
    }]
}

# Sending request to SkyScanner API
response = requests.post(url, headers=headers, json=payload)

# Checking if the response status is successful
if response.status_code == 200:
    try:
        # Get the JSON response
        data = response.json()

        # Print the full response to inspect its structure
        print("Full Response:")
        print(data)

        # Check if there are flights in the response
        carriers = data["data"]["itineraries"][0]["legs"][0]["carriers"]["marketing"]
        carrier_names = [carrier["name"] for carrier in carriers]

        price_formatted = data["data"]["itineraries"][0]["price"]["formatted"]
        print(carrier_names[0], price_formatted)
    except ValueError as e:
        # Handle JSON parsing errors
        print("Failed to parse JSON:", e)
        print("Response text:", response.text)
else:
    # Handle failed requests
    print(f"Failed to retrieve data: {response.status_code}")
    print("Response text:", response.text)