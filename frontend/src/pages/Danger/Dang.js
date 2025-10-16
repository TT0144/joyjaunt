import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkDangerByLocation } from "../../services/api";

const Danger = () => {
  const [loading, setLoading] = useState(false);
  const [locationLoading, setLocationLoading] = useState(false);
  const [error, setError] = useState(null);
  const [location, setLocation] = useState(null);
  const navigate = useNavigate();

  // 現在地を取得する関数
  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError("お使いのブラウザは位置情報をサポートしていません");
      return;
    }

    setLocationLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setLocation({ latitude, longitude });
        setLocationLoading(false);
        
        // 自動的に危険度チェックを実行
        await checkDangerByCoordinates(latitude, longitude);
      },
      (err) => {
        setLocationLoading(false);
        switch (err.code) {
          case err.PERMISSION_DENIED:
            setError("位置情報の取得が拒否されました。ブラウザの設定を確認してください。");
            break;
          case err.POSITION_UNAVAILABLE:
            setError("位置情報が利用できません。");
            break;
          case err.TIMEOUT:
            setError("位置情報の取得がタイムアウトしました。");
            break;
          default:
            setError("位置情報の取得中にエラーが発生しました。");
        }
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  };

  // サーバーから危険度情報を取得する関数
  const checkDangerByCoordinates = async (latitude, longitude) => {
    setLoading(true);
    setError(null);
    try {
      const data = await checkDangerByLocation(latitude, longitude);
      console.log("Received Data:", data);

      // 検出された場所を表示用に保存
      if (data.location) {
        setLocation({
          latitude: data.location.lat,
          longitude: data.location.lon,
          city: data.location.city,
          country: data.location.country
        });
      }

      // `is_dangerous`に応じてリダイレクト
      if (data.danger && data.danger.is_dangerous) {
        navigate("/warning", { state: { dangerData: data } });
      } else {
        navigate("/safe", { state: { dangerData: data } });
      }
    } catch (err) {
      setError(err.message || "危険度の確認中にエラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h1>危険度チェック</h1>
      
      <div style={{ marginBottom: "20px" }}>
        <button 
          onClick={getCurrentLocation} 
          disabled={loading || locationLoading}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: loading || locationLoading ? "not-allowed" : "pointer",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "5px"
          }}
        >
          {locationLoading ? "位置情報を取得中..." : loading ? "危険度を確認中..." : "現在地の危険度をチェック"}
        </button>
      </div>

      {location && (
        <div style={{ 
          marginTop: "20px", 
          padding: "15px", 
          backgroundColor: "#f0f0f0", 
          borderRadius: "5px" 
        }}>
          <h3>検出された位置情報</h3>
          {location.city && location.country && (
            <p><strong>場所:</strong> {location.city}, {location.country}</p>
          )}
          <p><strong>緯度:</strong> {location.latitude?.toFixed(6)}</p>
          <p><strong>経度:</strong> {location.longitude?.toFixed(6)}</p>
        </div>
      )}

      {error && (
        <div style={{ 
          marginTop: "20px", 
          padding: "15px", 
          backgroundColor: "#ffebee", 
          color: "#c62828",
          borderRadius: "5px",
          border: "1px solid #ef5350"
        }}>
          <strong>エラー:</strong> {error}
        </div>
      )}

      <div style={{ marginTop: "20px", fontSize: "14px", color: "#666" }}>
        <p>
          ℹ️ このボタンをクリックすると、ブラウザが現在地の位置情報を取得し、
          その場所の危険度を自動的に判定します。
        </p>
        <p>
          ⚠️ 位置情報の使用を許可するよう求められた場合は、「許可」を選択してください。
        </p>
      </div>
    </div>
  );
};

export default Danger;
