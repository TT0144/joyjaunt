import React from "react";
import "./ErrorMessage.css";

const ErrorMessage = ({ type = "error", message, onClose }) => {
  if (!message) return null;

  const icons = {
    error: "❌",
    warning: "⚠️",
    info: "ℹ️",
    success: "✅",
  };

  return (
    <div className={`error-message error-message--${type}`}>
      <span className="error-message__icon">{icons[type]}</span>
      <span className="error-message__text">{message}</span>
      {onClose && (
        <button className="error-message__close" onClick={onClose}>
          ✕
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
