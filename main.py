import streamlit as st
from openai import OpenAI

client = OpenAI(api_key='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')
# Title of the app
st.title("AI Travel Planner")

# Input fields
price_point = st.text_input("Price point: ")
duration = st.text_input("Duration: ")
number_of_people = st.text_input("Number of people: ")

# Button to generate the travel plan
if st.button("Generate Travel Plan"):
    # Check if all inputs are filled
    if price_point and duration and number_of_people:
        # Compose the prompt for OpenAI API
        prompt = (
            f"Plan a travel itinerary based on these details:\n"
            f"Price point: {price_point}\n"
            f"Duration: {duration} days\n"
            f"Number of people: {number_of_people}\n\n"
            f"Provide recommendations for destinations, activities, and a brief day-by-day itinerary."
        )

        # Make the OpenAI API call

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[{"role":"system", "content":prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        travel_plan = response.choices[0].message.content
        st.subheader("Your AI-Generated Travel Plan:")
        st.write(travel_plan)


    else:
        st.warning("Please fill in all fields.")
