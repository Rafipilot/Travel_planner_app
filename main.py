import streamlit as st
import openai

st.title("AI Travel Planner")

price_point = st.text_input("Price point: ")
Duration = st.text_input("Duration: ")
number_of_people = st.text_input("Number of people: ")

