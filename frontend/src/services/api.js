// API サービスユーティリティ
// 全てのAPI呼び出しを統一管理

import API_URL from "./config";

/**
 * APIエラークラス
 */
export class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = "APIError";
    this.status = status;
    this.data = data;
  }
}

/**
 * 統一されたfetchラッパー
 * @param {string} endpoint - APIエンドポイント
 * @param {object} options - fetchオプション
 * @returns {Promise} レスポンスデータ
 */
export const apiFetch = async (endpoint, options = {}) => {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  };

  const url = endpoint.startsWith("http") ? endpoint : `${API_URL}${endpoint}`;

  try {
    const response = await fetch(url, { ...defaultOptions, ...options });

    // レスポンスがJSONでない場合も処理
    const contentType = response.headers.get("content-type");
    const isJson = contentType && contentType.includes("application/json");

    const data = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      throw new APIError(
        data.error || data.message || "リクエストエラー",
        response.status,
        data
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }

    // ネットワークエラーなど
    throw new APIError(
      "サーバーに接続できません。ネットワークを確認してください。",
      0,
      { originalError: error.message }
    );
  }
};

/**
 * GET リクエスト
 */
export const apiGet = (endpoint, params = {}) => {
  const queryString = new URLSearchParams(params).toString();
  const url = queryString ? `${endpoint}?${queryString}` : endpoint;
  return apiFetch(url, { method: "GET" });
};

/**
 * POST リクエスト
 */
export const apiPost = (endpoint, data) => {
  return apiFetch(endpoint, {
    method: "POST",
    body: JSON.stringify(data),
  });
};

/**
 * PUT リクエスト
 */
export const apiPut = (endpoint, data) => {
  return apiFetch(endpoint, {
    method: "PUT",
    body: JSON.stringify(data),
  });
};

/**
 * DELETE リクエスト
 */
export const apiDelete = (endpoint) => {
  return apiFetch(endpoint, { method: "DELETE" });
};

// === 具体的なAPIエンドポイント ===

/**
 * 国一覧を取得
 */
export const getCountries = () => {
  return apiGet("/api/location/countries");
};

/**
 * 国別の都市一覧を取得
 */
export const getCitiesByCountry = (countryCode) => {
  return apiGet("/api/location/cities", { country_code: countryCode });
};

/**
 * 国別の都市詳細を取得
 */
export const getCityDetailsByCountry = (countryCode) => {
  return apiGet(`/api/location/cities/${countryCode}`);
};

/**
 * リアルタイム危険度チェック
 */
export const checkRealtimeDanger = (country, city) => {
  return apiPost("/api/danger/check_realtime_danger", { country, city });
};

/**
 * 位置情報ベース危険度チェック
 * @param {number} latitude - 緯度
 * @param {number} longitude - 経度
 */
export const checkDangerByLocation = (latitude, longitude) => {
  return apiPost("/api/danger/check_danger_by_location", {
    latitude,
    longitude,
  });
};

/**
 * 場所別ニュース取得
 */
export const getLocationNews = (country, city) => {
  return apiPost("/api/news/location_news", { country, city });
};

/**
 * 総合旅行情報取得
 */
export const getTravelInfo = (country, city) => {
  return apiPost("/api/danger/travel_info", { country, city });
};

/**
 * 天気予報取得(GET)
 */
export const getWeatherForecast = (city) => {
  return apiGet("/api/weather/weather_forecast", { city });
};

/**
 * 旅行計画用天気予報取得(GET)
 */
export const getWeatherForTravelPlan = (city) => {
  return apiGet("/api/weather/weather_forecast_for_travel_plan", { city });
};

/**
 * ユーザー登録
 */
export const registerUser = (userData) => {
  return apiPost("/api/auth/register", userData);
};

/**
 * ログイン
 */
export const loginUser = (credentials) => {
  return apiPost("/api/auth/login", credentials);
};

/**
 * ユーザー情報取得(要認証)
 */
export const getUserInfo = (token) => {
  return apiFetch("/api/auth/user-info", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

/**
 * トークン更新
 */
export const refreshToken = (refreshToken) => {
  return apiFetch("/api/auth/refresh", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${refreshToken}`,
    },
  });
};

// デフォルトエクスポート
const apiService = {
  get: apiGet,
  post: apiPost,
  put: apiPut,
  delete: apiDelete,
  // Specific endpoints
  getCountries,
  getCitiesByCountry,
  getCityDetailsByCountry,
  checkRealtimeDanger,
  checkDangerByLocation,
  getLocationNews,
  getTravelInfo,
  getWeatherForecast,
  getWeatherForTravelPlan,
  registerUser,
  loginUser,
  getUserInfo,
  refreshToken,
};

export default apiService;
