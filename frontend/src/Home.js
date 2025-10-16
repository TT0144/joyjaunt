import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { MapPin } from "lucide-react";
import Loading from "./Loading";
import ErrorMessage from "./components/ErrorMessage";
import {
  checkRealtimeDanger,
  getCityByCountry,
  getWeatherByCity,
} from "./services/api";
import "./home.css";

// 各画像のインポート
import clearImage from "./image/clear.png";
import rainImage from "./image/rain.png";
import snowImage from "./image/snow.png";
import cloudImage from "./image/cloud.png";
import mistImage from "./image/mist.png";

function Home() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [weatherData, setWeatherData] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedCountryName, setSelectedCountryName] = useState("");
  const [city, setCity] = useState("");
  const [dangerStatus, setDangerStatus] = useState("判定中");
  const [error, setError] = useState(null);
  const [passportStatus, setPassportStatus] = useState({
    isValid: true,
    message: "OK",
  });
  const [visaStatus, setVisaStatus] = useState({
    isValid: true,
    message: "OK 免除対象 (90日間ビザなしで入国できます。)",
  });

  console.log(visaStatus);
  console.log(passportStatus);

  // パスポートの有効期限チェック
  const checkPassportValidity = useCallback((expiryDate) => {
    if (!expiryDate)
      return { isValid: false, message: "NG パスポート情報がありません" };

    const today = new Date();
    const expiry = new Date(expiryDate);
    const sixMonthsFromNow = new Date();
    sixMonthsFromNow.setMonth(today.getMonth() + 6);

    if (expiry < today) {
      return {
        isValid: false,
        message: "NG パスポートの有効期限が切れています",
      };
    } else if (expiry < sixMonthsFromNow) {
      return {
        isValid: false,
        message: "NG パスポートの有効期限が6ヶ月以内です",
      };
    }
    return {
      isValid: true,
      message: "OK",
    };
  }, []);

  // ビザ要件チェック
  const checkVisaRequirements = useCallback((countryCode) => {
    const visaExemptCountries = countryCode;

    if (visaExemptCountries.includes(countryCode)) {
      return {
        isValid: true,
        message: "OK 免除対象 (90日間ビザなしで入国できます。)",
      };
    }
    return {
      isValid: false,
      message: "NG ビザの取得が必要です",
    };
  }, []);

  const getDangerScore = useCallback(async () => {
    try {
      setDangerStatus("判定中...");
      setError(null);
      const data = await checkRealtimeDanger(selectedCountryName, city);
      setDangerStatus(data.is_dangerous ? "危険" : "安全");
    } catch (error) {
      console.error("危険度スコアの取得エラー:", error);
      setDangerStatus("不明");
      setError(error.message);
    }
  }, [selectedCountryName, city]);

  const fetchWeatherData = async (city) => {
    try {
      setError(null);
      const data = await getWeatherByCity(city);
      setWeatherData(data);
    } catch (error) {
      console.error("天気データの取得エラー:", error);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const country = localStorage.getItem("selectedCountry") || "JP";
    const countryName = localStorage.getItem("selectedCountryName") || "Japan";
    const savedCity = localStorage.getItem("selectedCity") || "Tokyo";
    const passportExpiry = localStorage.getItem("passportExpiry");

    console.log(
      "取得したデータ:",
      country,
      countryName,
      savedCity,
      passportExpiry
    );

    setSelectedCountry(country);
    setSelectedCountryName(countryName);
    setCity(savedCity);

    setPassportStatus(checkPassportValidity(passportExpiry));
    setVisaStatus(checkVisaRequirements(country));
    localStorage.setItem("passportExpiry", "2025-11-01");
  }, [checkPassportValidity, checkVisaRequirements]);

  useEffect(() => {
    const loadCountryData = async () => {
      if (!selectedCountry) return;

      try {
        setError(null);
        getDangerScore();
        const cities = await getCityByCountry(selectedCountry);
        if (cities && cities.length > 0 && !city) {
          setCity(cities[0].Name);
        }
        setVisaStatus(checkVisaRequirements(selectedCountry));
      } catch (error) {
        console.error("都市データ取得エラー:", error);
        setError(error.message);
      }
    };

    loadCountryData();
  }, [selectedCountry, checkVisaRequirements, city, getDangerScore]);

  useEffect(() => {
    if (city) {
      fetchWeatherData(city);
      localStorage.setItem("selectedCity", city); // 変更された都市名をローカルストレージに保存
    }
  }, [city]);

  const weatherIconClick = () => {
    navigate("./Weather", {
      state: {
        selectedCountry,
        selectedCountryName,
        selectedCity: city,
      },
    });
  };

  const handleCardClick = () => {
    if (dangerStatus === "危険") {
      navigate("./warn"); // 危険ならWarning.jsへ遷移
    } else if (dangerStatus === "安全") {
      navigate("./Safe"); // 安全ならSafe.jsへ遷移
    } else {
    }
  };

  const getWeatherImage = (weather) => {
    if (!weather) return mistImage;

    if (weather.includes("Rain")) {
      return rainImage;
    } else if (weather.includes("Cloud")) {
      return cloudImage;
    } else if (weather.includes("Clear") || weather.includes("Shine")) {
      return clearImage;
    } else if (weather.includes("Snow")) {
      return snowImage;
    } else {
      return mistImage;
    }
  };
  return (
    <div className="App">
      {error && (
        <ErrorMessage
          type="error"
          message={error}
          onClose={() => setError(null)}
        />
      )}
      {isLoading ? (
        <Loading />
      ) : (
        <div className="happ-container">
          <div className="h-container">
            <div className="card">
              <div
                className="card-1"
                onClick={handleCardClick}
                style={{
                  cursor: "pointer",
                  backgroundColor:
                    dangerStatus === "危険"
                      ? "#D11C2C"
                      : dangerStatus === "判定中" ||
                        dangerStatus === "判定中..."
                      ? "#007BFF"
                      : "#4CAF50",
                }}
              >
                <span className="card-1Text">{dangerStatus}</span>
                <MapPin
                  style={{
                    width: "6rem",
                    height: "6rem",
                    marginBottom: "2rem",
                  }}
                />
              </div>

              <div className="weatherInfo" onClick={weatherIconClick}>
                <div className="locat">
                  <h2 className="cityName">{weatherData?.name}</h2>
                  <h3 className="cityRegion">{city}</h3>
                  <div className="temperature">{weatherData?.main.temp}°C</div>
                </div>
                <div className="icon">
                  <img
                    src={getWeatherImage(weatherData?.weather[0]?.main)}
                    alt={weatherData?.weather[0]?.main || "No data"}
                    className="weatherIcon"
                  />
                </div>
              </div>

              <div className="details">
                <p className="detailsParagraph">
                  ビザ:{" "}
                  <span
                    className={visaStatus.isValid ? "greenText" : "redText"}
                  >
                    {visaStatus.message}
                  </span>
                </p>
                <p className="detailsParagraph">
                  パスポートの有効期限:{" "}
                  <span
                    className={passportStatus.isValid ? "greenText" : "redText"}
                  >
                    {passportStatus.message}
                  </span>
                  {!passportStatus.isValid && (
                    <span className="warningText">
                      <br></br>※渡航には有効なパスポートが必要です
                    </span>
                  )}
                </p>
                <p className="detailsParagraph">通貨: JPY : MYR 1 : 0.0309</p>
                <p className="detailsParagraph">
                  支払い方法:
                  クレジットカードやモバイル決済が使われていますが、現金も主流です。
                </p>
                <p className="detailsParagraph">
                  電圧とプラグ: 240V、タイプG。海外旅行用の変換プラグ:{" "}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
