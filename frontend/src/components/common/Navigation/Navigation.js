import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import "./Navigation.css";

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);
  const isLoggedIn = !!localStorage.getItem("token");

  const navItems = [
    { path: "/", label: "ホーム", requireAuth: true },
    { path: "/tour", label: "ツアー", requireAuth: true },
    { path: "/weather", label: "天気", requireAuth: true },
    { path: "/setting", label: "設定", requireAuth: true },
  ];

  const toggleMenu = () => setIsOpen(!isOpen);

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/login-signup";
  };

  return (
    <nav className="navigation">
      <div className="navigation__container">
        <div className="navigation__brand">
          <h1>JoyJaunt</h1>
        </div>

        <button
          className="navigation__toggle"
          onClick={toggleMenu}
          aria-label="メニューを開く"
        >
          <span className={`hamburger ${isOpen ? "hamburger--open" : ""}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        <div
          className={`navigation__menu ${
            isOpen ? "navigation__menu--open" : ""
          }`}
        >
          <ul className="navigation__list">
            {navItems.map(
              (item) =>
                (!item.requireAuth || isLoggedIn) && (
                  <li key={item.path} className="navigation__item">
                    <NavLink
                      to={item.path}
                      className={({ isActive }) =>
                        `navigation__link ${
                          isActive ? "navigation__link--active" : ""
                        }`
                      }
                      onClick={() => setIsOpen(false)}
                    >
                      {item.label}
                    </NavLink>
                  </li>
                )
            )}
            {!isLoggedIn ? (
              <li className="navigation__item">
                <NavLink
                  to="/login-signup"
                  className="navigation__link navigation__link--primary"
                  onClick={() => setIsOpen(false)}
                >
                  ログイン
                </NavLink>
              </li>
            ) : (
              <li className="navigation__item">
                <button
                  onClick={handleLogout}
                  className="navigation__link navigation__link--logout"
                >
                  ログアウト
                </button>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
