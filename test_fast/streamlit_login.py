import base64
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your local image
local_image_path = "pexels-donaldtong94-189296.jpg"
base64_local_image = get_base64_of_bin_file(local_image_path)

def register():
    st.title("Register")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register"):
        response = requests.post(f"{API_URL}/register/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("User registered successfully")
        else:
            st.error(response.json()["detail"])

def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Login successful")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.experimental_rerun()
        else:
            st.error(response.json()["detail"])

def add_hotel():
    st.title("Add Hotel")
    name = st.text_input("Hotel Name")
    location = st.text_input("Location")
    price = st.number_input("Price", min_value=0, step=1)
    if st.button("Add Hotel"):
        response = requests.post(f"{API_URL}/hotels/", json={"name": name, "location": location, "price": price})
        if response.status_code == 200:
            st.success("Hotel added successfully")
        else:
            st.error("Failed to add hotel")

def view_hotels():
    st.title("View Hotels")
    response = requests.get(f"{API_URL}/hotels/")
    if response.status_code == 200:
        hotels = response.json()
        for hotel in hotels:
            st.write(f"ID: {hotel['id']}")
            st.write(f"Name: {hotel['name']}")
            st.write(f"Location: {hotel['location']}")
            st.write(f"Price: {hotel['price']}")
            if st.button(f"Delete Hotel {hotel['id']}"):
                delete_response = requests.delete(f"{API_URL}/hotels/{hotel['id']}")
                if delete_response.status_code == 200:
                    st.success(f"Hotel {hotel['id']} deleted successfully")
                else:
                    st.error("Failed to delete hotel")

def update_hotel():
    st.title("Update Hotel")
    hotel_id = st.number_input("Hotel ID", min_value=0, step=1)
    name = st.text_input("Hotel Name")
    location = st.text_input("Location")
    price = st.number_input("Price", min_value=0, step=1)
    if st.button("Update Hotel"):
        response = requests.put(f"{API_URL}/hotels/{hotel_id}", json={"name": name, "location": location, "price": price})
        if response.status_code == 200:
            st.success("Hotel updated successfully")
        else:
            st.error("Failed to update hotel")

def show_hotel_management_options(username):
    st.sidebar.write(f"Logged in as {username}")
    option = st.sidebar.selectbox("Choose an option", ["Add Hotel", "View Hotels", "Update Hotel"])
    if option == "Add Hotel":
        add_hotel()
    elif option == "View Hotels":
        view_hotels()
    elif option == "Update Hotel":
        update_hotel()
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.experimental_rerun()

# Main function to control flow
def main():
    st.sidebar.title("Hotel Management System")

    # Injecting the custom CSS
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_local_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""

    if st.session_state['logged_in']:
        show_hotel_management_options(st.session_state['username'])
    else:
        page = st.sidebar.selectbox("Choose an option", ["Login", "Register"])
        if page == "Login":
            login()
        elif page == "Register":
            register()

if __name__ == "__main__":
    main()
