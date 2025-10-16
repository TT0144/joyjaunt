import React from "react";
import "./Loading.css";

const Loading = () => {
  return (
    <div className="loading">
      <div className="loading__spinner"></div>
      <p className="loading__text">読み込み中...</p>
    </div>
  );
};

export default Loading;
