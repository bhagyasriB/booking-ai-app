import React, { useState } from "react";
import axios from "axios";
import './Booking.scss';

function Booking() {
  const [fromCity, setFromCity] = useState("");
  const [toCity, setToCity] = useState("");
  const [result, setResult] = useState("");
  const [seatPreference, setSeatPreference] = useState("Window");
  const [loading, setLoading] = useState(false);

   const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult("");

    try {
      const res = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          from_city: fromCity,
          to_city: toCity,
          seat_preference: seatPreference,
        }),
      });

      const data = await res.json();
      setResult(data.summary || "No result found.");
    } catch (err) {
      setResult("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex flex-col items-center justify-center text-gray-800 p-6">
      <div className="w-full max-w-lg bg-white shadow-2xl rounded-3xl p-8 border border-blue-100">
        <h1 className="text-3xl font-bold text-center text-blue-700 mb-6 heading">
          ✈️ AI Travel Booking Assistant
        </h1>
<div className="form-conainer card">
        <form onSubmit={handleSearch} className="space-y-5">
          {/* From City */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              From City
            </label>
            <input
              type="text"
              value={fromCity}
              onChange={(e) => setFromCity(e.target.value)}
              placeholder="Enter departure city"
              required
              className="w-full border border-gray-300 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          {/* To City */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              To City
            </label>
            <input
              type="text"
              value={toCity}
              onChange={(e) => setToCity(e.target.value)}
              placeholder="Enter destination city"
              required
              className="w-full border border-gray-300 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          {/* Seat Preference */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              Seat Preference
            </label>
            <select
              value={seatPreference}
              onChange={(e) => setSeatPreference(e.target.value)}
              className="w-full border border-gray-300 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option>Window</option>
              <option>Aisle</option>
              <option>Middle</option>
            </select>
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 rounded-xl font-semibold text-white transition transform hover:scale-[1.02] ${
              loading
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 shadow-md"
            }`}
          >
            {loading ? "Booking..." : "Search & Book"}
          </button>
        </form>

        {/* Result Section */}
        {result && (
          <div className="mt-6 bg-gradient-to-r from-green-50 to-green-100 border border-green-300 rounded-2xl shadow-inner p-5 whitespace-pre-line">
            <h2 className="text-lg font-semibold text-green-700 mb-2">
              Booking Summary
            </h2>
            <p className="text-gray-800 leading-relaxed">{result}</p>
          </div>
        )}
      </div>

     </div>
    </div>
  );
}

export default Booking;
