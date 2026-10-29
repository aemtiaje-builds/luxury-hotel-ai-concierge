import time
import streamlit as st

st.set_page_config(
    page_title="The Willow House",
    page_icon="🏨",
    layout="centered"
)

# ---------- Design ----------
st.markdown("""
<style>
    .stApp {
        background: #f4efe6;
        color: #243b35;
    }

    h1, h2, h3, p, label {
        color: #243b35 !important;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #243b35;
        color: white;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Hotel information ----------
ROOM_PRICES = {
    "Deluxe": 8500,
    "Suite": 14500,
    "Garden": 11000
}

st.title("🏨 The Willow House")
st.subheader("Your Virtual Hotel Concierge")

st.write(
    "Welcome! Explore our demo rooms, ask hotel questions, "
    "and try submitting a booking inquiry."
)

st.info(
    "Portfolio demo: this is a fictional hotel. "
    "Prices and services are examples, not live offers."
)

# ---------- Rooms ----------
st.header("Explore Our Rooms")

room = st.selectbox(
    "Choose your preferred room",
    list(ROOM_PRICES.keys())
)

st.subheader(f"{room} — ৳{ROOM_PRICES[room]:,} per night")

st.write(
    "Check-in: 3 PM  \n"
    "Check-out: 11 AM  \n"
    "Breakfast: 7 AM–10:30 AM"
)

st.divider()

# ---------- Demo booking inquiry ----------
st.header("📅 Try a Booking Inquiry")

st.caption(
    "This public demo does not save or transmit your personal details. "
    "Use fictional details when testing."
)

with st.form("demo_booking_form"):
    guest_name = st.text_input("Guest name (use a fictional name)")
    check_in = st.date_input("Check-in date")
    check_out = st.date_input("Check-out date")
    guests = st.number_input(
        "Number of guests",
        min_value=1,
        max_value=10,
        value=2
    )

    submitted = st.form_submit_button("Try Demo Booking")

if submitted:
    if not guest_name.strip():
        st.error("Please enter a name for the demo.")
    elif check_out <= check_in:
        st.error("Check-out must be after check-in.")
    else:
        st.success("🎉 Demo inquiry completed successfully!")
        st.write("### Your demo summary")
        st.write(f"**Guest:** {guest_name.strip()}")
        st.write(f"**Room:** {room}")
        st.write(f"**Check-in:** {check_in}")
        st.write(f"**Check-out:** {check_out}")
        st.write(f"**Guests:** {guests}")
        st.warning(
            "This is only a demonstration. No reservation was created."
        )

st.divider()


# ---------- Gemini AI Concierge ----------
import os
from google import genai

st.header("🤖 AI Concierge Chat")
st.caption("Powered by Gemini AI")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Create the Gemini client once and reuse it
@st.cache_resource
def get_gemini_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)

try:
    client = get_gemini_client()
except Exception:
    client = None

# Display previous messages
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything about your hotel stay...")

if prompt:
    st.session_state.chat_messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if client is None:
            answer = (
                "The AI concierge is not configured yet. "
                "Please check the Gemini API key in Streamlit secrets."
            )
            st.error(answer)
        else:
            try:
                # Include recent conversation so follow-up questions
                # make sense to the AI.
                recent_messages = st.session_state.chat_messages[-10:]

                conversation = "\n".join(
                    f"{'Guest' if m['role'] == 'user' else 'Concierge'}: "
                    f"{m['content']}"
                    for m in recent_messages
                )

                instructions = """
You are the friendly virtual concierge for The Willow House,
a fictional hotel demo in Dhaka, Bangladesh.

Hotel information:
- Deluxe room: ৳8,500 per night
- Garden room: ৳11,000 per night
- Suite: ৳14,500 per night and have luxurious amenities, 5g starlink wifi, tv with premium subscriptions, warm water, and a mini bar.
- Check-in: 3 PM
- Check-out: 11 AM
- Breakfast: 7 AM to 10:30 AM and menu includes continental and local dishes like paratha, omelette, fresh fruits , chai, coffee, and fresh juices.

Rules:
- Be warm, natural, helpful, and concise.
- Understand the guest's meaning, not just keywords.
- Use the conversation history to answer follow-up questions.
- You may answer general hospitality questions, too.
- These hotel details are demo examples, not verified real offers.
- Never claim to check live room availability or confirm a real booking.
- Never invent hotel policies or facilities that are not provided.
- If you don't know a hotel-specific answer, say so and suggest
  contacting the hotel team.
- This is a demonstration; no real reservation is created.
"""
            
                with st.spinner("Generating response..."):
                  start_time = time.perf_counter()

                response = client.interactions.create(
                    model="gemini-3.5-flash-lite",
                    input=(
                      instructions
                      + "\n\nConversation so far:\n"
                      + conversation
                      + "\n\nConcierge:"
    ),
                    timeout=60000,  
)               
                elapsed = time.perf_counter() - start_time

                answer = response.output_text or (
                  "Sorry, I couldn't generate a response. "
                  "Please try asking in a different way."
)
                st.markdown(answer)
                st.caption(f"Response generated in {elapsed:.2f} seconds")

            except Exception as e:
                answer = (
                    "Sorry, the AI service couldn't respond just now. "
                    "Please try again in a moment."
                )
                st.error(answer)
                st.error(f"Technical error: {type(e).__name__}: {e}")
                # Technical details are shown only while testing locally.
                if os.environ.get("STREAMLIT_CLOUD") != "true":
                    st.caption(f"Debug details: {e}")

    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": answer
    })

st.caption(
    "Portfolio project • Fictional hotel in Dhaka, Bangladesh • "
    "Gemini AI demo"
)

