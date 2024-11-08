import streamlit as st
import requests
from openai import OpenAI
from datetime import datetime

from secret import openai_key
from secret import rapidAPI_key


st.set_page_config(layout="wide")

def get_flight_price(departure, destination, depart_date, number_of_people):
    # SkyScanner API URL
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-multi-city"

    # Headers for API authentication
    headers = {
        'x-rapidapi-key': rapidAPI_key,
        'x-rapidapi-host': "sky-scanner3.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    # Dynamic payload based on user inputs
    payload = {
        "market": "US",
        "locale": "en-US",
        "currency": "USD",
        "adults": number_of_people,
        "children": 0,
        "infants": 0,
        "cabinClass": "economy",
        "stops": ["direct"],
        "sort": "cheapest_first",
        "flights": [{
            "fromEntityId": departure,
            "toEntityId": destination,
            "departDate": depart_date
        }]
    }

    # Request to SkyScanner API
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            carriers = data["data"]["itineraries"][0]["legs"][0]["carriers"]["marketing"]
            carrier_names = [carrier["name"] for carrier in carriers]
            price_formatted = data["data"]["itineraries"][0]["price"]["formatted"]
            return carrier_names[0], price_formatted
        except Exception as e:
            st.error("Unable to get flight data: ", e)
  
            return None, None
    else:
        st.error(f"Failed to retrieve data: {response.status_code}")
        return None, None

client = OpenAI(api_key=openai_key)


# Title of the app
st.title("AI Travel Planner")
big_left, big_right = st.columns([0.3, 0.7])

with big_left:
    # Input fields
    price_point = st.text_input("Enter your budget:")
    #duration = st.text_input("Trip duration (days):")
    number_of_people = st.text_input("Number of people traveling:")
    departure = st.text_input("Departure Airport Code (e.g., LHR for London Heathrow):")
    destination = st.text_input("Destination Airport Code (e.g., JFK for New York JFK):")
    depart_date = st.date_input("Departure Date:")
    return_date = st.date_input("Return Date:")

    # Convert depart_date and return_date to strings
    d1 = datetime.strptime(str(depart_date), "%Y-%m-%d")
    d2 = datetime.strptime(str(return_date), "%Y-%m-%d")

    duration = (d2 - d1).days
    print("duration:", duration)


with big_right:
    # Retrieve flight details based on user inputs
    if departure and destination and depart_date and return_date:
        flight, flight_price = get_flight_price(departure, destination, str(depart_date), number_of_people)
        if flight and flight_price:
            st.write(f"**Flight Information**")
            st.write(f"Carrier: {flight}")
            st.write(f"Price: {flight_price}")
        return_flight, return_flight_price = get_flight_price(destination, destination, str(depart_date), number_of_people)
    else:
        st.warning("Please enter departure, destination, and date to check flight prices.")

    # Generate travel plan button
    if st.button("Generate Travel Plan"):
        if price_point and duration and number_of_people and departure and destination:
            prompt = (
                f"You are an expert travel planner. Create a fun, personalized, and budget-friendly itinerary based on the following details:\n\n"
                f"- **Budget**: {price_point}$\n"
                f"- **Trip duration**: {duration} days\n"
                f"- **Number of travelers**: {number_of_people}\n"
                f"- **Departure**: {departure}\n"
                f"- **Destination**: {destination}\n\n"
                f"**Flight Info**:\n"
                f"- Carrier: {flight}\n"
                f"- Price: {flight_price}\n\n"
                f"**Accommodation**: Recommend budget-friendly hotels with links and brief descriptions.\n"
                f"**Activities**: Suggest popular attractions and fun activities within the budget, with links.\n"
                f"**Itinerary**: Create a day-by-day plan, balancing sightseeing and relaxation. Include meal suggestions and travel tips. "
                f"Make sure it's within budget and feasible for the trip duration."
                F"At the end add up all the costs and compare with the budget"
            )

            # Make the OpenAI API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )

            travel_plan = response.choices[0].message.content
            st.subheader("Your AI-Generated Travel Plan:")
            st.write(travel_plan)

        else:
            st.warning("Please fill in all fields to generate a travel plan.")

