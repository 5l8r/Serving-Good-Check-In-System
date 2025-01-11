import streamlit as st
import requests

# Apps Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwpFxeL0t37Rxc6bg-WNYgps9wsQcw7swuKupuhUXQCjKJX1U10TxdFB6J1wClDHxZh/exec"

# Helper function to normalize phone numbers
def normalize_phone(phone):
    phone = re.sub(r"[^\d]", "", phone)  # Remove non-numeric characters
    if len(phone) == 10:
        return f"+1{phone}"  # Add country code if missing
    if len(phone) == 11 and phone.startswith("1"):
        return f"+{phone}"  # Add '+' if missing
    return phone

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

# Market Info Section
st.header("Market Info")
market_response = fetch_backend(f"{SCRIPT_URL}?marketInfo=true")
if "error" in market_response:
    st.error(market_response["error"])
else:
    st.markdown(f"**Next Market:** {market_response['date']} at {market_response['startTime']}")
    st.markdown(f"**Check-In Window:** {market_response['checkInStart']} - {market_response['checkInEnd']}")

# Check-In Section
st.header("Check In")
phone_or_email = st.text_input("Enter Email or Phone", placeholder="Email or Phone Number")
check_in_button = st.button("Check In")

if check_in_button:
    if not phone_or_email:
        st.error("Please enter your email or phone.")
    else:
        normalized_phone = normalize_phone(phone_or_email)
        payload = {"input": normalized_phone}
        response = fetch_backend(SCRIPT_URL, method="POST", payload=payload)
        if "error" in response:
            st.error(response["error"])
        elif "numberAssigned" in response:
            st.success(f"Your spot is #{response['numberAssigned']}.")
        elif "standby" in response:
            st.info(response["message"])