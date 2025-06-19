import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  NavLink,
} from "react-router-dom";
import Home from "./Home";
import Danger from "./Dang";
import Safety from "./Safe";
import Warning from "./Warning";
import Weather from "./Weather";
import LoginSignup from "./LoginSignup"; // LoginSignup をインポート
import AccountSummary from "./AccountSummary";
import Tour from "./tour";
import Setting from "./Setting";
import "./index.css";

function App() {
  return (
    <Router>
      {/* <nav>
        <NavLink
          to="/"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Home
        </NavLink>{" "}
        |
        <NavLink
          to="/dang"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Danger
        </NavLink>{" "}
        |
        <NavLink
          to="/weather"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Weather
        </NavLink>{" "}
        |
        <NavLink
          to="/login-signup"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          LoginSignup
        </NavLink>
      </nav> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dang" element={<Danger />} />
        <Route path="/weather" element={<Weather />} />
        <Route path="/safe" element={<Safety />} />
        <Route path="/warn" element={<Warning />} />
        <Route path="/login-signup" element={<LoginSignup />} />
        <Route path="/AccountSummary" element={<AccountSummary />} />
        <Route path="/tour" element={<Tour />} />
        <Route path="/settings" element={<Setting />} />
        {/* LoginSignup ページ */}
        <Route path="*" element={<h1>404: Page Not Found</h1>} />
      </Routes>
    </Router>
  );
}

export default App;
