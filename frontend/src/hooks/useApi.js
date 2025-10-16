// カスタムフック: API呼び出しの管理
import { useState, useCallback } from "react";
import { APIError } from "../services/api";

/**
 * API呼び出しを管理するカスタムフック
 * ローディング状態、エラーハンドリングを自動化
 */
export const useApi = (apiFunction) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (...args) => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiFunction(...args);
        setData(result);
        return result;
      } catch (err) {
        const errorMessage =
          err instanceof APIError
            ? err.message
            : "エラーが発生しました。もう一度お試しください。";
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    data,
    loading,
    error,
    execute,
    reset,
  };
};

/**
 * 複数のAPIを順次実行するフック
 */
export const useApiQueue = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);

  const execute = useCallback(async (apiCalls) => {
    try {
      setLoading(true);
      setError(null);
      setResults([]);

      const allResults = [];
      for (const apiCall of apiCalls) {
        const result = await apiCall();
        allResults.push(result);
      }

      setResults(allResults);
      return allResults;
    } catch (err) {
      const errorMessage =
        err instanceof APIError ? err.message : "エラーが発生しました。";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, error, results, execute };
};

/**
 * フォーム送信用のフック
 */
export const useFormSubmit = (submitFunction) => {
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const submit = useCallback(
    async (formData) => {
      try {
        setSubmitting(true);
        setError(null);
        setSuccess(false);

        const result = await submitFunction(formData);

        setSuccess(true);
        return result;
      } catch (err) {
        const errorMessage =
          err instanceof APIError
            ? err.message
            : "送信に失敗しました。もう一度お試しください。";
        setError(errorMessage);
        throw err;
      } finally {
        setSubmitting(false);
      }
    },
    [submitFunction]
  );

  const reset = useCallback(() => {
    setSuccess(false);
    setError(null);
    setSubmitting(false);
  }, []);

  return {
    submitting,
    success,
    error,
    submit,
    reset,
  };
};

export default useApi;
