import streamlit as st
import requests
import re  # For phone normalization

# Apps Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzS_cD47EPl-OyLy5cO-G2Y9w766pGw8KDJdoPJ4ZJkPQkyqTKW9Vqzvqq_AysWY5Dj/exec"

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

# Market Info Section
st.header("Market Info")
response = fetch_backend(f"{SCRIPT_URL}?marketInfo=true")
if "error" in response:
    st.error(response["error"])
else:
    is_open = response.get("isOpen", False)
    next_market = response.get("nextMarket", {})
    
    # Display the next market
    st.markdown(f"**Next Market:** {next_market.get('date', 'TBD')} at {next_market.get('startTime', 'TBD')}")
    st.markdown(f"**Check-In Window:** {next_market.get('checkInStart', 'TBD')} - {next_market.get('checkInEnd', 'TBD')}")
    
    # Show if check-in is open or closed
    if is_open:
        st.markdown("## Check In: **OPEN**", unsafe_allow_html=True, color="green")
    else:
        st.markdown("## Check In: **CLOSED**", unsafe_allow_html=True, color="red")


# Check-In Section
st.header("Check In")
phone = st.text_input("Enter Phone Number")
if st.button("Check In"):
    if not phone:
        st.error("Please enter your phone number.")
    else:
        processing_placeholder = st.empty()  # Create a placeholder
        processing_placeholder.info("Processing check-in...")  # Show the "Processing check-in..." message
        normalized_phone = normalize_phone(phone)
        payload = {"input": normalized_phone}
        response = fetch_backend(SCRIPT_URL, method="POST", payload=payload)
        processing_placeholder.empty()  # Clear the "Processing check-in..." message
        if "error" in response:
            st.error(response["error"])
        elif "success" in response:
            st.success(response["success"])
        else:
            st.info("Unexpected response. Please try again.")
