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

# Helper function to convert military time to 12-hour time
def convert_to_12_hour(time_str):
    if not time_str or ":" not in time_str:
        return time_str  # Return as-is if invalid
    hours, minutes = map(int, time_str.split(":"))
    period = "AM" if hours < 12 else "PM"
    hours = hours % 12 or 12  # Convert 0 to 12 for 12-hour time
    return f"{hours}:{minutes:02d} {period}"

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
    
    # Convert military times to 12-hour format
    start_time = convert_to_12_hour(next_market.get("startTime", "TBD"))
    check_in_start = convert_to_12_hour(next_market.get("checkInStart", "TBD"))
    check_in_end = convert_to_12_hour(next_market.get("checkInEnd", "TBD"))

    # Display the next market
    st.markdown(f"**Next Market:** {next_market.get('date', 'TBD')} at {start_time}")
    st.markdown(f"**Check-In Window:** {check_in_start} - {check_in_end}")
    
# Show if check-in is open or closed
if is_open:
    st.markdown('<span style="font-size: 24px;">Check In: <span style="color: green;">OPEN</span></span>', unsafe_allow_html=True)
else:
    st.markdown('<span style="font-size: 24px;">Check In: <span style="color: red;">CLOSED</span></span>', unsafe_allow_html=True)



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
