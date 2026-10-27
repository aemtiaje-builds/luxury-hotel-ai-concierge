import ollama
import streamlit as st
import csv
from pathlib import Path

st.set_page_config(
    page_title="The Willow House",
    page_icon="🏨",
    layout="centered"
)



st.markdown("""
<style>
    .stApp {
        background: #f4efe6;
        color: #243b35;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stForm"] {
        background: #e9e1d4;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #d4c8b5;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
    }

    h1, h2, h3, p, label {
        color: #243b35 !important;
    }

    input, textarea, [data-baseweb="select"] > div {
        background-color: #fffdf8 !important;
        color: #243b35 !important;
        border-radius: 8px !important;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #243b35 !important;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #36594e !important;
        color: #ffffff !important;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)



st.title("🏨 The Willow House")
st.subheader("Your Virtual Hotel Concierge")

st.write(
    "Welcome! I can help you explore our rooms, "
    "check hotel information, and submit a booking inquiry."
)

st.success("Our virtual concierge is ready!")
st.header("Explore Our Rooms")

room = st.selectbox(
    "Choose your preferred room",
    ["Deluxe", "Suite", "Garden"]
)

st.write(f"You selected: {room}")

room_prices = {
    "Deluxe": 8500,
    "Suite": 14500,
    "Garden": 11000
}

st.write(f"You selected: {room}")
st.subheader(f"Price: ৳{room_prices[room]:,} per night")



st.divider()
st.header("📅 Submit a Booking Inquiry")

with st.form("booking_form"):
    guest_name = st.text_input("Your full name")

    check_in = st.date_input("Check-in date")
    check_out = st.date_input("Check-out date")

    guests = st.number_input(
        "Number of guests",
        min_value=1,
        max_value=10,
        value=2
    )

    submitted = st.form_submit_button("Submit Inquiry")

    if submitted:
        if not guest_name.strip():
            st.error("Please enter your name.")
        elif check_out <= check_in:
            st.error("Check-out must be after check-in.")
        
        else:
            st.success("Your booking inquiry has been received!")

            file_path = Path(__file__).with_name("bookings.csv")

            booking = {
                "guest_name": guest_name,
                "room": room,
                "check_in": str(check_in),
                "check_out": str(check_out),
                "guests": guests,
    }

            file_exists = file_path.exists()

            with file_path.open("a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=booking.keys())

                if not file_exists:
                  writer.writeheader()
 
                writer.writerow(booking)

            st.success("Booking inquiry saved successfully!")

            st.write(f"**Guest:** {guest_name}")
            st.write(f"**Room:** {room}")
            st.write(f"**Check-in:** {check_in}")
            st.write(f"**Check-out:** {check_out}")
            st.write(f"**Guests:** {guests}")



st.caption("Demo project • Fictional hotel in Dhaka, Bangladesh")

st.divider()


owner_password = st.text_input(
    "Enter owner password",
    type="password",
    key="owner_password"
)

owner_secret = st.secrets["OWNER_PASSWORD"]

if owner_password == owner_secret:
    st.header("🔐 Hotel Owner Dashboard")

    file_path = Path(__file__).with_name("bookings.csv")

    if file_path.exists():
        try:
            with file_path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                bookings = list(reader)

            if bookings:
                st.write("### 📊 Booking Overview")

                total_bookings = len(bookings)
                st.metric("Total Booking Inquiries", total_bookings)

                total_guests = 0

                for booking in bookings:
                    try:
                        total_guests += int(booking.get("guests", 0))
                    except (ValueError, TypeError):
                        continue

                st.metric("Total Guests Requested", total_guests)

                st.success(
                    f"You have received {total_bookings} booking inquiries."
                )

                st.write("### 🏨 Room Preferences")

                room_counts = {}

                for booking in bookings:
                    room = booking.get("room", "Unknown")
                    room_counts[room] = room_counts.get(room, 0) + 1

                if room_counts:
                    st.bar_chart(room_counts)

                st.dataframe(bookings, use_container_width=True)

                csv_data = file_path.read_bytes()

                st.download_button(
                    label="📥 Download Booking Records",
                    data=csv_data,
                    file_name="hotel_booking_records.csv",
                    mime="text/csv",
                )

            else:
                st.info("No booking inquiries yet.")

        except (OSError, csv.Error) as error:
            st.error(f"Could not read bookings: {error}")

    else:
        st.info("No booking inquiries have been saved yet.")

elif owner_password:
    st.error("Incorrect password.")





st.divider()
st.header("🤖 AI Concierge Chat")
st.write("Ask our virtual concierge a question.")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about rooms, breakfast, check-in..."):
    st.session_state.chat_messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
      with st.spinner("Concierge is thinking..."):
       prompt_lower = prompt.lower()

    if "price" in prompt_lower or "cost" in prompt_lower or "rate" in prompt_lower:
        if "suite" in prompt_lower:
            answer = "The Suite room costs ৳14,500 per night."
        elif "deluxe" in prompt_lower:
            answer = "The Deluxe room costs ৳8,500 per night."
        elif "garden" in prompt_lower:
            answer = "The Garden room costs ৳11,000 per night."
        else:
            answer = (
                "Our demo room rates are: Deluxe ৳8,500, "
                "Suite ৳14,500, and Garden ৳11,000 per night."
            )

    elif "check-in" in prompt_lower or "check in" in prompt_lower:
        answer = "Check-in time is 3 PM."

    elif "check-out" in prompt_lower or "check out" in prompt_lower:
        answer = "Check-out time is 11 AM."

    elif "breakfast" in prompt_lower:
        answer = "Breakfast is served from 7 AM to 10:30 AM."

    else:
        try:
            response = ollama.chat(
                model="llama3.2:1b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly virtual concierge for "
                            "The Willow House, a fictional hotel in Dhaka. "
                            "Its demo prices are Deluxe ৳8,500, Suite ৳14,500, "
                            "and Garden ৳11,000 per night. Check-in is 3 PM, "
                            "check-out is 11 AM, and breakfast is 7 AM to "
                            "10:30 AM. Never claim to check live availability "
                            "or confirm reservations. If unsure, say so."
                        )
                    },
                    *st.session_state.chat_messages
                ]
            )
            answer = response["message"]["content"]

        except Exception as error:
            answer = f"Sorry, the local AI could not respond: {error}"

    st.markdown(answer)

    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": answer
    })


