import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navigation from "./components/Navigation";
import Home from "./Home";
import Danger from "./Dang";
import Safety from "./Safe";
import Warning from "./Warning";
import Weather from "./Weather";
import LoginSignup from "./LoginSignup";
import AccountSummary from "./AccountSummary";
import Tour from "./tour";
import Setting from "./Setting";
import NotFound from "./NotFound";
import "./index.css";

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
