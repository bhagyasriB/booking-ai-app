from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_flow import run_booking

app = FastAPI()

# ✅ Allow frontend (React) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookingRequest(BaseModel):
    from_city: str
    to_city: str
    seat_preference: str

@app.post("/search")
def search_flight_and_hotel(req: BookingRequest):
    summary = run_booking(req.from_city, req.to_city, req.seat_preference)
    return {"summary": summary}
