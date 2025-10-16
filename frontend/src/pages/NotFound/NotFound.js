// 404 Not Found ページ
import React from "react";
import { useNavigate } from "react-router-dom";
import "./NotFound.css";

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="not-found">
      <div className="not-found__content">
        <div className="not-found__animation">
          <span className="not-found__icon">🧭</span>
          <div className="not-found__circle"></div>
        </div>
        <h1 className="not-found__title">404</h1>
        <h2 className="not-found__subtitle">ページが見つかりません</h2>
        <p className="not-found__description">
          お探しのページは存在しないか、移動または削除された可能性があります。
        </p>
        <div className="not-found__actions">
          <button
            className="not-found__button not-found__button--primary"
            onClick={() => navigate("/")}
          >
            🏠 ホームに戻る
          </button>
          <button
            className="not-found__button not-found__button--secondary"
            onClick={() => navigate(-1)}
          >
            ← 前のページに戻る
          </button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
