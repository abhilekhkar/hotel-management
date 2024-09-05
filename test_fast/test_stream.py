streamlit_login.pyimport streamlit as st
from PIL import Image
import base64

# Function to get the base64 of the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your local image
local_image_path = "pexels-donaldtong94-189296.jpg"
base64_local_image = get_base64_of_bin_file(local_image_path)

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

# Your Streamlit code here
st.title("Streamlit App with Background")
st.write("This is an example of a Streamlit app with a custom background image.")

