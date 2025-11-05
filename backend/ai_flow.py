from dotenv import load_dotenv
import os
import random
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Initialize the LLM (OpenAI via LangChain)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define workflow state
class BookingState(dict):
    location_from: str
    location_to: str
    travel_date: str
    seat_preference: str
    flights: list
    hotels: list
    best_flight: dict
    best_hotel: dict
    transaction_id: str
    summary: str


# 1️⃣ Get Flights
def get_flights(state: BookingState):
    state["flights"] = [
    {"id": 1, "name": "Air India", "from": "Delhi", "to": "Paris", "price": 450, "rating": 4.5},
    {"id": 2, "name": "Indigo", "from": "Delhi", "to": "Paris", "price": 400, "rating": 4.2},
    {"id": 3, "name": "Vistara", "from": "Delhi", "to": "Paris", "price": 480, "rating": 4.7},
    {"id": 4, "name": "SpiceJet", "from": "Delhi", "to": "Paris", "price": 370, "rating": 3.9},
    {"id": 5, "name": "Lufthansa", "from": "Mumbai", "to": "Berlin", "price": 500, "rating": 4.6}
    ]
    return state


# 2️⃣ Get Hotels
def get_hotels(state: BookingState):
    state["hotels"] = [
    {"id": 1, "name": "Hotel Le Grand", "city": "Paris", "price": 150, "rating": 4.8},
    {"id": 2, "name": "Budget Stay", "city": "Paris", "price": 80, "rating": 3.9},
    {"id": 3, "name": "Comfort Inn", "city": "Paris", "price": 120, "rating": 4.4},
    {"id": 4, "name": "Luxury Palace", "city": "Paris", "price": 250, "rating": 4.9},
    {"id": 5, "name": "Downtown Suites", "city": "Berlin", "price": 160, "rating": 4.3}
    ]
    return state


# 3️⃣ Ask OpenAI (LangChain) to pick best options
def select_best_options(state: BookingState):
    prompt = ChatPromptTemplate.from_template("""
    You are an expert travel planner.
    The user wants to travel from {location_from} to {location_to} on {travel_date}.
    They prefer a {seat_preference} seat.
    
    Choose the best balance between rating and price from the options below.
    
    Flights: {flights}
    Hotels: {hotels}

    Return a JSON object with chosen flight and hotel:
    {{
      "flight": {{ ... }},
      "hotel": {{ ... }}
    }}
    """)

    chain = prompt | llm
    result = chain.invoke({
        "location_from": state["location_from"],
        "location_to": state["location_to"],
        "travel_date": state["travel_date"],
        "seat_preference": state["seat_preference"],
        "flights": state["flights"],
        "hotels": state["hotels"]
    })
    import json
    try:
        parsed = json.loads(result.content)
        state["best_flight"] = parsed.get("flight", {})
        state["best_hotel"] = parsed.get("hotel", {})
    except:
        state["best_flight"] = state["flights"][0]
        state["best_hotel"] = state["hotels"][0]
    return state


# 4️⃣ Simulate Transaction Step
def set_transaction(state: BookingState):
    state["transaction_id"] = f"TXN-{random.randint(100000,999999)}"
    return state


# 5️⃣ Generate Final Summary
def generate_summary(state: BookingState):
    prompt = ChatPromptTemplate.from_template("""
    You are an AI assistant confirming a travel booking.

    Flight: {best_flight}
    Hotel: {best_hotel}
    Transaction ID: {transaction_id}
    Travel Date: {travel_date}
    From: {location_from}
    To: {location_to}
    Seat Preference: {seat_preference}

    Create a detailed and friendly booking summary for the user.
    """)

    chain = prompt | llm
    result = chain.invoke({
        "best_flight": state["best_flight"],
        "best_hotel": state["best_hotel"],
        "transaction_id": state["transaction_id"],
        "travel_date": state["travel_date"],
        "location_from": state["location_from"],
        "location_to": state["location_to"],
        "seat_preference": state["seat_preference"]
    })
    state["summary"] = result.content
    return state


# 🧩 Build LangGraph workflow
workflow = StateGraph(BookingState)
workflow.add_node("get_flights", get_flights)
workflow.add_node("get_hotels", get_hotels)
workflow.add_node("select_best_options", select_best_options)
workflow.add_node("set_transaction", set_transaction)
workflow.add_node("generate_summary", generate_summary)

workflow.add_edge("get_flights", "get_hotels")
workflow.add_edge("get_hotels", "select_best_options")
workflow.add_edge("select_best_options", "set_transaction")
workflow.add_edge("set_transaction", "generate_summary")
workflow.add_edge("generate_summary", END)

workflow.add_edge("__start__", "get_flights")

graph = workflow.compile()


def run_booking_flow(location_from, location_to, travel_date, seat_preference):
    state = BookingState({
        "location_from": location_from,
        "location_to": location_to,
        "travel_date": travel_date,
        "seat_preference": seat_preference
    })
    result = graph.invoke(state)
    return result["summary"]
