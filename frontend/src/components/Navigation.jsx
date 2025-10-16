// ナビゲーションコンポーネント
import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('passportExpiry');
    localStorage.removeItem('country');
    navigate('/login-signup');
    closeMenu();
  };

  const isLoggedIn = !!localStorage.getItem('access_token');

  const navItems = [
    { path: '/', label: 'ホーム', icon: '🏠' },
    { path: '/tour', label: '旅行計画', icon: '✈️' },
    { path: '/weather', label: '天気予報', icon: '🌤️' },
    { path: '/dang', label: '危険情報', icon: '⚠️' },
  ];

  const userItems = isLoggedIn
    ? [
        { path: '/AccountSummary', label: 'アカウント', icon: '👤' },
        { path: '/settings', label: '設定', icon: '⚙️' },
      ]
    : [
        { path: '/login-signup', label: 'ログイン', icon: '🔐' },
      ];

  return (
    <>
      <nav className="navigation">
        <div className="navigation__container">
          <div className="navigation__brand">
            <NavLink to="/" className="navigation__logo">
              <span className="navigation__logo-icon">🌍</span>
              <span className="navigation__logo-text">JoyJaunt</span>
            </NavLink>
          </div>

          {/* ハンバーガーメニューボタン */}
          <button
            className={`navigation__toggle ${isOpen ? 'navigation__toggle--open' : ''}`}
            onClick={toggleMenu}
            aria-label="メニューを開く"
            aria-expanded={isOpen}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          {/* ナビゲーションメニュー */}
          <div className={`navigation__menu ${isOpen ? 'navigation__menu--open' : ''}`}>
            <ul className="navigation__list">
              {navItems.map((item) => (
                <li key={item.path} className="navigation__item">
                  <NavLink
                    to={item.path}
                    className={({ isActive }) =>
                      `navigation__link ${isActive ? 'navigation__link--active' : ''}`
                    }
                    onClick={closeMenu}
                  >
                    <span className="navigation__link-icon">{item.icon}</span>
                    <span className="navigation__link-text">{item.label}</span>
                  </NavLink>
                </li>
              ))}
            </ul>

            <ul className="navigation__list navigation__list--user">
              {userItems.map((item) => (
                <li key={item.path} className="navigation__item">
                  <NavLink
                    to={item.path}
                    className={({ isActive }) =>
                      `navigation__link ${isActive ? 'navigation__link--active' : ''}`
                    }
                    onClick={closeMenu}
                  >
                    <span className="navigation__link-icon">{item.icon}</span>
                    <span className="navigation__link-text">{item.label}</span>
                  </NavLink>
                </li>
              ))}
              {isLoggedIn && (
                <li className="navigation__item">
                  <button
                    className="navigation__link navigation__link--logout"
                    onClick={handleLogout}
                  >
                    <span className="navigation__link-icon">🚪</span>
                    <span className="navigation__link-text">ログアウト</span>
                  </button>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>

      {/* オーバーレイ */}
      {isOpen && (
        <div
          className="navigation__overlay"
          onClick={closeMenu}
          aria-hidden="true"
        ></div>
      )}
    </>
  );
};

export default Navigation;
