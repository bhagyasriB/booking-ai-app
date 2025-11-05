import statistics
import random
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

# ---- SAMPLE DATA ----
flights = [
    {"id": 1, "name": "Air India", "from": "Delhi", "to": "Paris", "price": 450, "rating": 4.5},
    {"id": 2, "name": "Indigo", "from": "Delhi", "to": "Paris", "price": 400, "rating": 4.2},
    {"id": 3, "name": "Vistara", "from": "Delhi", "to": "Paris", "price": 480, "rating": 4.7},
    {"id": 4, "name": "SpiceJet", "from": "Delhi", "to": "Paris", "price": 370, "rating": 3.9},
    {"id": 5, "name": "Lufthansa", "from": "Mumbai", "to": "Berlin", "price": 500, "rating": 4.6},
]

hotels = [
    {"id": 1, "name": "Hotel Le Grand", "city": "Paris", "price": 150, "rating": 4.8},
    {"id": 2, "name": "Budget Stay", "city": "Paris", "price": 80, "rating": 3.9},
    {"id": 3, "name": "Comfort Inn", "city": "Paris", "price": 120, "rating": 4.4},
    {"id": 4, "name": "Luxury Palace", "city": "Paris", "price": 250, "rating": 4.9},
    {"id": 5, "name": "Downtown Suites", "city": "Berlin", "price": 160, "rating": 4.3},
]

# ---- BOOKING STATE ----
class BookingState(TypedDict):
    from_city: str
    to_city: str
    seat_preference: str
    best_flight: Dict
    best_hotel: Dict
    booked: bool
    seat_number: str
    transaction_id: str
    summary: str

# ---- HELPERS ----
def find_best(items: List[Dict], price_key="price") -> Dict:
    prices = [i[price_key] for i in items]
    median_price = statistics.median(prices)
    normal_max = median_price * 1.2
    candidates = [i for i in items if i[price_key] <= normal_max]
    candidates.sort(key=lambda x: (-x["rating"], x[price_key]))
    return candidates[0] if candidates else items[0]

# ---- GRAPH NODES ----
def select_flight(state: BookingState):
    available = [f for f in flights if f["from"].lower() == state["from_city"].lower() and f["to"].lower() == state["to_city"].lower()]
    if not available:
        return {**state, "best_flight": {"name": "No flights found", "price": 0, "rating": 0}}
    best = find_best(available)
    return {**state, "best_flight": best}

def select_hotel(state: BookingState):
    available = [h for h in hotels if h["city"].lower() == state["to_city"].lower()]
    if not available:
        return {**state, "best_hotel": {"name": "No hotels found", "price": 0, "rating": 0}}
    best = find_best(available)
    return {**state, "best_hotel": best}

def assign_seat(state: BookingState):
    pref = state.get("seat_preference", "Window")
    seat_map = {"Window": ["A", "F"], "Aisle": ["C", "D"], "Middle": ["B", "E"]}
    seat_letter = random.choice(seat_map.get(pref, ["A", "F"]))
    seat_number = f"{random.randint(1, 30)}{seat_letter}"
    return {**state, "seat_number": seat_number}

def take_transaction(state: BookingState):
    # Simulate payment gateway
    flight_price = state["best_flight"].get("price", 0)
    hotel_price = state["best_hotel"].get("price", 0)
    total = flight_price + hotel_price
    transaction_id = f"TXN-{random.randint(100000,999999)}"
    print(f"Processed transaction {transaction_id} for amount ${total}")
    return {**state, "transaction_id": transaction_id}

def auto_book(state: BookingState):
    return {**state, "booked": True}

def summarize_booking(state: BookingState):
    f, h = state["best_flight"], state["best_hotel"]
    booked_text = "✅ Booking Confirmed!" if state.get("booked") else "❌ Not booked yet."
    summary = (
        f"{booked_text}\n\n"
        f"✈️ Flight: {f['name']} (${f['price']}, {f['rating']}⭐)\n"
        f"🪟 Seat: {state.get('seat_preference', '-')}, Seat No: {state.get('seat_number', '-')}\n"
        f"🏨 Hotel: {h['name']} (${h['price']}, {h['rating']}⭐)\n"
        f"💳 Transaction ID: {state.get('transaction_id', '-')}\n"
        f"Route: {state['from_city']} ➡️ {state['to_city']}\n"
        "Both are best rated and within normal price range."
    )
    return {**state, "summary": summary}

# ---- GRAPH DEFINITION ----
workflow = StateGraph(BookingState)
workflow.add_node("select_flight", select_flight)
workflow.add_node("select_hotel", select_hotel)
workflow.add_node("assign_seat", assign_seat)
workflow.add_node("take_transaction", take_transaction)
workflow.add_node("auto_book", auto_book)
workflow.add_node("summarize_booking", summarize_booking)

workflow.add_edge("select_flight", "select_hotel")
workflow.add_edge("select_hotel", "assign_seat")
workflow.add_edge("assign_seat", "take_transaction")
workflow.add_edge("take_transaction", "auto_book")
workflow.add_edge("auto_book", "summarize_booking")
workflow.add_edge("summarize_booking", END)
workflow.set_entry_point("select_flight")

booking_graph = workflow.compile()

def run_booking(from_city: str, to_city: str, seat_preference: str):
    result = booking_graph.invoke({
        "from_city": from_city,
        "to_city": to_city,
        "seat_preference": seat_preference
    })
    return result["summary"]
