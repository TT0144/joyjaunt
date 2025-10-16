import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Danger = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // サーバーから危険度情報を取得する関数
  const fetchDangerInfo = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/check_realtime_danger",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ country: "CN" }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch danger information");
      }

      const data = await response.json();
      console.log("Received Data:", data);

      // `is_dangerous`に応じてリダイレクト
      if (data.is_dangerous) {
        navigate("/warning");
      } else {
        navigate("/safe");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Danger Check</h1>
      <button onClick={fetchDangerInfo} disabled={loading}>
        {loading ? "Checking..." : "Check Danger"}
      </button>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
    </div>
  );
};

export default Danger;
