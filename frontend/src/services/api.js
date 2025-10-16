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
  return apiGet("/countries");
};

/**
 * 国別の都市一覧を取得
 */
export const getCitiesByCountry = (countryCode) => {
  return apiGet("/get_cities_by_country", { country_code: countryCode });
};

/**
 * 国別の都市詳細を取得
 */
export const getCityDetailsByCountry = (countryCode) => {
  return apiGet(`/get_city_by_country/${countryCode}`);
};

/**
 * リアルタイム危険度チェック
 */
export const checkRealtimeDanger = (country, city) => {
  return apiPost("/check_realtime_danger", { country, city });
};

/**
 * 場所別ニュース取得
 */
export const getLocationNews = (country, city) => {
  return apiPost("/get_location_news", { country, city });
};

/**
 * 総合旅行情報取得
 */
export const getTravelInfo = (country, city) => {
  return apiPost("/travel_info", { country, city });
};

/**
 * 天気予報取得(POST)
 */
export const getWeatherForecast = (city) => {
  return apiPost("/weather_forecast", { city });
};

/**
 * 旅行計画用天気予報取得(GET)
 */
export const getWeatherForTravelPlan = (city) => {
  return apiGet("/weather_forecast_for_travel_plan", { city });
};

/**
 * ユーザー登録
 */
export const registerUser = (userData) => {
  return apiPost("/register", userData);
};

/**
 * ログイン
 */
export const loginUser = (credentials) => {
  return apiPost("/login", credentials);
};

/**
 * ユーザー情報取得(要認証)
 */
export const getUserInfo = (token) => {
  return apiFetch("/get_user_info", {
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
  return apiFetch("/refresh", {
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
