import streamlit as st
import requests
import re  # Add this import for regular expressions

# Apps Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwr0Ouehr69KXEYZQ_oJ6qLOhALKWMvvfdAj7GslSrrryTkVAPuelXZgjC1UDhKPYVe/exec"

# Helper function to normalize phone numbers
def normalize_phone(phone):
    if not phone:
        return None
    phone = re.sub(r"[^\d]", "", phone)  # Remove non-numeric characters
    if len(phone) == 10:  # Add country code if missing
        return "+1" + phone
    elif len(phone) == 11 and phone.startswith("1"):  # Normalize US numbers
        return "+" + phone
    return phone  # Return as is for other formats

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

# Market Info Section (Automatically fetches on page load)
st.header("Market Info")
response = fetch_backend(f"{SCRIPT_URL}?marketInfo=true")
if "error" in response:
    st.error(response["error"])
else:
    st.markdown(f"**Next Market:** {response['date']} at {response['startTime']}")
    st.markdown(f"**Check-In Window:** {response['checkInStart']} - {response['checkInEnd']}")

# Check-In Section
st.header("Check In")
phone = st.text_input("Enter Phone Number")  # Updated to only request phone numbers
if st.button("Check In"):
    if not phone:
        st.error("Please enter your phone number.")
    else:
        st.info("Processing check-in...")  # Temporary info message
        normalized_phone = normalize_phone(phone)
        payload = {"input": normalized_phone}
        response = fetch_backend(SCRIPT_URL, method="POST", payload=payload)
        st.write(response)  # Debugging: Show the response
        if "error" in response:
            st.error(response["error"])
        elif "success" in response:
            st.success(response["success"])
        else:
            st.info("Please wait for further instructions.")
