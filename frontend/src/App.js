import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navigation from "./components/common/Navigation";
import Home from "./pages/Home";
import Danger from "./pages/Danger";
import Safety from "./pages/Safe";
import Warning from "./pages/Warning";
import Weather from "./pages/Weather";
import LoginSignup from "./pages/Auth";
import AccountSummary from "./pages/Account";
import Tour from "./pages/Tour";
import Setting from "./Setting";
import NotFound from "./pages/NotFound";
import "./styles/index.css";

function App() {
  return (
    <Router>
      <Navigation />
      <main className="app-main">
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
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
