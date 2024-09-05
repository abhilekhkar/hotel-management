import streamlit as st
import requests
from datetime import datetime

backend_url = "http://localhost:8000"

def register_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f"{backend_url}/register/", json=data)
    return response.json()

def sign_in_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f"{backend_url}/signin/", json=data)
    return response.json()

def get_bookings():
    response = requests.get(f"{backend_url}/bookings/")
    return response.json()

def create_booking(name, check_in, check_out, room_type):
    data = {
        "name": name,
        "check_in": check_in,
        "check_out": check_out,
        "room_type": room_type
    }
    response = requests.post(f"{backend_url}/bookings/", json=data)
    return response.json()

def update_booking(booking_id, name, check_in, check_out, room_type):
    data = {
        "name": name,
        "check_in": check_in,
        "check_out": check_out,
        "room_type": room_type
    }
    response = requests.put(f"{backend_url}/bookings/{booking_id}", json=data)
    return response.json()

def delete_booking(booking_id):
    response = requests.delete(f"{backend_url}/bookings/{booking_id}")
    return response.json()

st.title("Hotel Booking Management")

menu = ["Register", "Sign In", "Create Booking", "View Bookings", "Update Booking", "Delete Booking"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        result = register_user(username, password)
        st.success(f"{result['message']}")

elif choice == "Sign In":
    st.subheader("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        result = sign_in_user(username, password)
        st.success(f"{result['message']}")

elif choice == "Create Booking":
    st.subheader("Add Booking")
    name = st.text_input("Name")
    check_in = st.date_input("Check-in Date")
    check_out = st.date_input("Check-out Date")
    room_type = st.selectbox("Room Type", ["Single", "Double", "Suite"])
    if st.button("Create Booking"):
        result = create_booking(name, check_in.isoformat(), check_out.isoformat(), room_type)
        st.success(f"Booking created: {result}")

elif choice == "View Bookings":
    st.subheader("View Bookings")
    bookings = get_bookings()
    for booking in bookings:
        st.write(f"Booking ID: {booking['id']}, Name: {booking['name']}, Check-in: {booking['check_in']}, Check-out: {booking['check_out']}, Room Type: {booking['room_type']}")

elif choice == "Update Booking":
    st.subheader("Update Booking")
    booking_id = st.number_input("Booking ID", min_value=1)
    name = st.text_input("Name")
    check_in = st.date_input("Check-in Date")
    check_out = st.date_input("Check-out Date")
    room_type = st.selectbox("Room Type", ["Single", "Double", "Suite"])
    if st.button("Update Booking"):
        result = update_booking(booking_id, name, check_in.isoformat(), check_out.isoformat(), room_type)
        st.success(f"Booking updated: {result}")

elif choice == "Delete Booking":
    st.subheader("Delete Booking")
    booking_id = st.number_input("Booking ID", min_value=1)
    if st.button("Delete Booking"):
        result = delete_booking(booking_id)
        st.success(f"Booking deleted: {result}")
