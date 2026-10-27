
import csv
from pathlib import Path


"""
Luxury Hotel AI Concierge — beginner portfolio project
Run with: python hotel_concierge.py
This is a rule-based demo, not a real AI model or WhatsApp integration.
"""

HOTEL = {
    "name": "The Willow House",
    "check_in": "3:00 PM",
    "check_out": "11:00 AM",
    "breakfast": "7:00 AM–10:30 AM",
    "wifi": "Willow_Guest",
    "wifi_password": "welcome2026",
    "currency": "BDT",
    "rooms": {
        "deluxe": 8500,
        "suite": 14500,
        "garden": 11000,
    },
}

FAQ = {
    "pool": "Our rooftop pool is open daily from 7:00 AM to 9:00 PM.",
    "parking": "Complimentary on-site parking is available for hotel guests.",
    "pet": "Please contact our team before arrival so we can confirm our current pet policy.",
    "location": "We're a fictional boutique hotel in Dhaka, Bangladesh. This demo does not represent a real property.",
    "cancellation": "Cancellation terms depend on the selected rate. Our team can confirm the terms before you book.",
    "breakfast": f"Breakfast is served from {HOTEL['breakfast']}.",
    "check in": f"Check-in begins at {HOTEL['check_in']}. Early check-in depends on availability.",
    "check-in": f"Check-in begins at {HOTEL['check_in']}. Early check-in depends on availability.",
    "check out": f"Check-out is by {HOTEL['check_out']}. Late check-out depends on availability.",
    "check-out": f"Check-out is by {HOTEL['check_out']}. Late check-out depends on availability.",
    "wifi": f"Guest Wi-Fi network: {HOTEL['wifi']}. Password: {HOTEL['wifi_password']}.",
    "wi-fi": f"Guest Wi-Fi network: {HOTEL['wifi']}. Password: {HOTEL['wifi_password']}.",
}

def save_booking(name, check_in, check_out, guests, room):
    file_path = Path(__file__).with_name("bookings.csv")

    booking = {
        "name": name,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "room": room,
    }

    file_exists = file_path.exists()

    with file_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=booking.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(booking)

    print("Concierge: Your booking inquiry has been saved successfully!")




def money(amount):
    return f"৳{amount:,.0f} per night"

def show_menu():
    print("\nYou can ask about:")
    print("  • room prices")
    print("  • check-in / check-out")
    print("  • breakfast, Wi-Fi, parking or pool")
    print("  • booking a room")
    print("  • talking to a human")
    print("Type 'quit' to leave.\n")

def answer(message):
    """Return a helpful reply based on simple keyword rules."""
    text = message.lower().strip()

    if any(word in text for word in ["human", "staff", "manager", "person", "agent"]):
        return ("HUMAN HANDOFF: Of course. I'll pass your request to our guest-relations "
                "team. In a real deployment, this would notify hotel staff.")

    if any(word in text for word in ["book", "reservation", "reserve"]):
        return ("I'd be happy to help with a booking inquiry. Please tell me your "
                "check-in date, check-out date, number of guests, and preferred room. "
                "This demo cannot check live availability or confirm a reservation.")

    if any(word in text for word in ["price", "cost", "rate", "room"]):
        prices = "\n".join(
            f"  • {name.title()} Room: {money(price)}"
            for name, price in HOTEL["rooms"].items()
        )
        return (f"Certainly! Here are our sample rates at {HOTEL['name']}:\n{prices}\n"
                "These are demo prices only and do not include taxes or confirm availability.")

    for keyword, reply in FAQ.items():
        if keyword in text:
            return reply

    if any(word in text for word in ["hello", "hi", "hey", "assalamu", "salam"]):
        return (f"Welcome to {HOTEL['name']}! I'm your virtual concierge. "
                "How may I make your stay more comfortable today?")

    return ("I'd love to help with that, but I don't have a verified answer in this demo. "
            "Would you like me to connect you with our guest-relations team?")

def collect_booking():
    print("\nConcierge: I'd be happy to record your booking inquiry.")

    name = input("Your name: ").strip()
    if not name:
       print("Concierge: Please enter your name.")
       return 
    check_in = input("Check-in date (YYYY-MM-DD): ").strip()
    check_out = input("Check-out date (YYYY-MM-DD): ").strip()
    from datetime import datetime

    try:
      start_date = datetime.strptime(check_in, "%Y-%m-%d")
      end_date = datetime.strptime(check_out, "%Y-%m-%d")

      if end_date <= start_date:
        print("Concierge: Check-out must be after check-in.")
        return

    except ValueError:
      print("Concierge: Please use YYYY-MM-DD for both dates.")
      return
    guests_text = input("Number of guests: ").strip()
    room = input("Preferred room (Deluxe/Suite/Garden): ").strip()
    if room.lower() not in ["deluxe", "suite", "garden"]:
       print("Concierge: Please choose Deluxe, Suite, or Garden.")
       return

    try:
        guests = int(guests_text)
        if guests < 1:
            print("Concierge: Please enter at least one guest.")
            return
    except ValueError:
        print("Concierge: Please enter the number of guests as a whole number.")
        return

    if not all([name, check_in, check_out, room]):
        print("Concierge: Please fill in every field.")
        return

    save_booking(name, check_in, check_out, guests, room)
    print("Concierge: Our team can follow up about availability and rates.")

def main():
    print("=" * 54)
    print(f"  Welcome to {HOTEL['name']} — Virtual Concierge")
    print("  Thoughtful service, available any time.")
    print("=" * 54)
    print("Concierge: Good day! How may I assist you?")
    show_menu()

    while True:
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nConcierge: Thank you for visiting. Have a lovely day!")
            break

        if message.lower() in {"quit", "exit", "bye"}:
            print("Concierge: Thank you for chatting with us. Have a lovely day!")
            break

        if not message:
            continue

        if any(word in message.lower() for word in ["book", "booking", "reservation", "reserve"]):
          collect_booking()
          continue

        print(f"\nConcierge: {answer(message)}\n")

if __name__ == "__main__":
    main()
