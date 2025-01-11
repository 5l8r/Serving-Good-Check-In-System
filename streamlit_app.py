import streamlit as st
import requests

# Apps Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxOC36jPr33RvQL-5HE4mGpFHFFF9O1pBqpmLi4MpkgEhXrRfJFKkwenjpLg_rMZo-p/exec"

# Helper function to interact with the backend
def fetch_backend(endpoint, method="GET", payload=None):
    try:
        if method == "POST":
            response = requests.post(endpoint, json=payload)
        else:
            response = requests.get(endpoint)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

# Streamlit UI
st.title("Non-Profit Check-In System")

# Sign-Up Section
st.header("Sign Up")
with st.form("signup_form"):
    first_name = st.text_input("First Name", placeholder="Enter your first name")
    email = st.text_input("Email", placeholder="Enter your email")
    phone = st.text_input("Phone", placeholder="Enter your phone number")
    signup_button = st.form_submit_button("Sign Up")

if signup_button:
    if not first_name or not email or not phone:
        st.error("All fields are required.")
    else:
        payload = {"signup": True, "firstName": first_name, "email": email, "phone": phone}
        response = fetch_backend(SCRIPT_URL, method="POST", payload=payload)
        if "error" in response:
            st.error(response["error"])
        else:
            st.success(response.get("success", "Sign-up successful!"))

# Market Info Section
st.header("Market Info")
market_info_button = st.button("Fetch Market Info")
if market_info_button:
    response = fetch_backend(f"{SCRIPT_URL}?marketInfo=true")
    if "error" in response:
        st.error(response["error"])
    else:
        st.markdown(f"**Next Market:** {response['date']} at {response['startTime']}")
        st.markdown(f"**Check-In Window:** {response['checkInStart']} - {response['checkInEnd']}")

# Check-In Section
st.header("Check In")
check_in_input = st.text_input("Enter Email or Phone")
check_in_button = st.button("Check In")

if check_in_button:
    if not check_in_input:
        st.error("Please enter your email or phone.")
    else:
        payload = {"input": check_in_input}
        response = fetch_backend(SCRIPT_URL, method="POST", payload=payload)
        if "error" in response:
            st.error(response["error"])
        elif "numberAssigned" in response:
            st.success(f"Your spot is #{response['numberAssigned']}.")
        elif "standby" in response:
            st.info(response["message"])
