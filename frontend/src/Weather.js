import React, { useState, useEffect } from "react";
import "./Weather.css";
import mapImage from "./image/map.png";
import cortImage from "./image/cort.png";
import jucketImage from "./image/jucket.png";
import longTImage from "./image/long-T.png";
import shortTImage from "./image/short-T.png";

import { useNavigate, useLocation } from "react-router-dom";
import clearImage from "./image/clear.png";
import rainImage from "./image/rain.png";
import showerrainImage from "./image/showerrain.png";
import snowImage from "./image/snow.png";
import cloudImage from "./image/cloud.png";
import thunderstormImage from "./image/thunderstorm.png";
import mistImage from "./image/mist.png";

const Weather = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [weather, setWeather] = useState([]);
  const [clothingRecommendation, setClothingRecommendation] = useState("");
  const [clothingImage, setClothingImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [countryName, setCountryName] = useState("");
  const [cityName, setCityName] = useState("");

  const API_URL = "http://10.108.0.4:5000";

  useEffect(() => {
    const storedCountryName = localStorage.getItem("selectedCountryName");
    const storedCity = localStorage.getItem("selectedCity");

    console.log("ローカルストレージから取得した国名:", storedCountryName); // デバッグログ
    console.log("ローカルストレージから取得した都市名:", storedCity); // デバッグログ

    setCountryName(storedCountryName || "");
    setCityName(storedCity || "");

    if (storedCity) {
      fetchWeatherForTravelPlan(storedCity);
    } else {
      console.error("都市名が指定されていません！");
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login-signup");
      return;
    }
  }, [navigate]);

  const fetchWeatherForTravelPlan = async (city) => {
    setLoading(true);
    try {
      console.log("天気取得中の都市:", city); // デバッグログ

      const response = await fetch(
        `${API_URL}/weather_forecast_for_travel_plan?city=${city}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        console.error(
          "APIレスポンスエラー:",
          response.status,
          response.statusText
        ); // デバッグログ
        throw new Error("天気データの取得に失敗しました");
      }

      const data = await response.json();

      if (
        data.forecast &&
        Array.isArray(data.forecast) &&
        data.forecast.length > 0
      ) {
        setWeather(data.forecast);
        generateClothingRecommendation(data.forecast[0]);
      } else {
        console.error("天気データが空です"); // デバッグログ
        setError("有効な天気データがありません");
      }
    } catch (error) {
      console.error("天気情報取得エラー:", error); // デバッグログ
    } finally {
      setLoading(false);
    }
  };

  const generateClothingRecommendation = (currentWeather) => {
    const temperature = currentWeather.temperature;
    const weatherCondition = currentWeather.weather;

    let recommendation = "";
    let clothingImage = null;

    if (temperature > 25) {
      recommendation = "Tシャツ、ショートパンツ";
      clothingImage = shortTImage;
    } else if (temperature >= 20) {
      recommendation = "薄手の長袖シャツ、ジーンズ";
      clothingImage = longTImage;
    } else if (temperature >= 10) {
      recommendation = "ジャケット、セーター";
      clothingImage = jucketImage;
    } else {
      recommendation = "厚手のコート、防寒具";
      clothingImage = cortImage;
    }

    if (weatherCondition.includes("雨")) {
      recommendation += "、傘やレインコートも必要です";
    }

    setClothingRecommendation(recommendation);
    setClothingImage(clothingImage); // 画像を設定
  };

  const getWeatherImage = (weather) => {
    // `weather` が undefined または null の場合、mistImage を返す
    if (!weather) return mistImage;

    // 天気情報に基づいて画像を返す
    if (weather.includes("雨")) {
      return rainImage; // 雨系のアイコン
    } else if (weather.includes("曇") || weather.includes("雲")) {
      return cloudImage; // 曇り系のアイコン
    } else if (weather.includes("晴")) {
      return clearImage; // 晴れ系のアイコン
    } else if (weather.includes("雪")) {
      return snowImage; // 雪系のアイコン
    } else {
      return mistImage; // その他（デフォルト）のアイコン
    }
  };

  return (
    <div className="app-container">
      <div className="container">
        {loading && <p>読み込み中...</p>}
        {error && <p className="error-message">{error}</p>}

        {weather.length > 0 && (
          <>
            <div className="location">
              <h1>{countryName}</h1>
              <h2>{cityName}</h2>
              <div className="temp">{weather[0].temperature}°C</div>
            </div>
            <div className="icon">
              <img
                src={getWeatherImage(weather[0].weather)}
                alt="Weather Icon"
              />
            </div>
            <div className="box2">
              <div className="box2-1">
                <div className="forecast">
                  {weather.map((forecast, index) => (
                    <div key={index}>
                      {new Date(forecast.date).toLocaleDateString("ja-JP", {
                        weekday: "short",
                      })}
                    </div>
                  ))}
                </div>
                <div className="forecast-icons">
                  {weather.map((forecast, index) => (
                    <div key={index}>
                      <img
                        src={getWeatherImage(forecast.weather)} // weather を適切に渡す
                        alt={`Weather forecast for ${forecast.date}`}
                      />
                    </div>
                  ))}
                </div>

                <div className="forecast-temp">
                  {weather.map((forecast, index) => (
                    <div key={index}>{forecast.temperature}°C</div>
                  ))}
                </div>
              </div>
              <div className="box2-2">
                <div className="clothing">
                  <h2>服装のおすすめ</h2>
                  <div className="clothing-box">
                    {clothingImage && (
                      <img src={clothingImage} alt="Clothing Suggestion" />
                    )}
                    <p>{clothingRecommendation}</p>
                  </div>
                </div>
              </div>
              <button
                className="back-button"
                onClick={() => window.history.back()}
              >
                戻る
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Weather;
