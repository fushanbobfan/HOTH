import React, { useState } from "react";

const TungShing = () => {
  const [date, setDate] = useState("");
  const [tungShingResult, setTungShingResult] = useState(null);
  const [fortune, setFortune] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    if (!date) return;
    
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/tungshing/${date}`);
      const data = await response.json();
      setTungShingResult(data);
    } catch (error) {
      console.error("Error fetching Tung Shing data:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHourlyFortune = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:5000/api/hourly_fortune", { method: "POST" });
      const data = await response.json();
      setFortune(data);
    } catch (error) {
      console.error("Error fetching hourly fortune:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDailyFortune = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:5000/api/daily_fortune", { method: "POST" });
      const data = await response.json();
      setFortune(data[0]);  // Expecting a list from Flask, so take the first item
    } catch (error) {
      console.error("Error fetching daily fortune:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMonthlyInfluence = async () => {
    try {
      setLoading(true);
      const now = new Date();
      const month = now.getMonth() + 1;
      const response = await fetch("http://127.0.0.1:5000/api/monthly_influence", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ month: month }),
      });
      const data = await response.json();
      setFortune({ monthly_influence: data.monthly_influence });
    } catch (error) {
      console.error("Error fetching monthly influence:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Tung Shing Calendar & Astrology</h1>
      
      <label>Select a Date:</label>
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <button onClick={fetchData}>Get Tung Shing Info</button>
      <button onClick={fetchHourlyFortune}>Get Hourly Fortune</button>
      <button onClick={fetchDailyFortune}>Get Daily Fortune</button>
      <button onClick={fetchMonthlyInfluence}>Get Monthly Influence</button>

      {loading && <p>Loading...</p>}

      {tungShingResult && (
        <div style={{ marginTop: "20px" }}>
          <h2>Tung Shing Results</h2>
          <p><strong>Lunar Date:</strong> {tungShingResult.lunar_date}</p>
          <p><strong>Good to do:</strong> {tungShingResult.auspicious.join(", ")}</p>
          <p><strong>Bad to do:</strong> {tungShingResult.inauspicious.join(", ")}</p>
        </div>
      )}

      {fortune && (
        <div style={{ marginTop: "20px" }}>
          <h2>Astrological Fortune</h2>
          {fortune.current_time && <p><strong>Current Time:</strong> {fortune.current_time}</p>}
          {fortune.sun_sign && <p><strong>Sun Sign:</strong> {fortune.sun_sign}</p>}
          {fortune.moon_sign && <p><strong>Moon Sign:</strong> {fortune.moon_sign}</p>}
          {fortune.ascendant && <p><strong>Ascendant:</strong> {fortune.ascendant}</p>}
          {fortune.monthly_influence && <p><strong>Monthly Influence:</strong> {fortune.monthly_influence}</p>}
          {fortune.suggestions && (
            <ul>
              {fortune.suggestions.map((s, index) => <li key={index}>{s}</li>)}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default TungShing;
