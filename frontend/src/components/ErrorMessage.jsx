// エラー表示コンポーネント
import React from 'react';
import './ErrorMessage.css';

/**
 * エラーメッセージコンポーネント
 * @param {string} message - エラーメッセージ
 * @param {string} type - エラータイプ (error, warning, info)
 * @param {function} onClose - 閉じるボタンのコールバック
 */
const ErrorMessage = ({ message, type = 'error', onClose }) => {
  if (!message) return null;

  const getIcon = () => {
    switch (type) {
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      case 'success':
        return '✅';
      default:
        return '❌';
    }
  };

  return (
    <div className={`error-message error-message--${type}`} role="alert">
      <span className="error-message__icon">{getIcon()}</span>
      <span className="error-message__text">{message}</span>
      {onClose && (
        <button
          className="error-message__close"
          onClick={onClose}
          aria-label="閉じる"
        >
          ×
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
