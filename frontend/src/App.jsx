import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginSignup from "./pages/LoginSignup";
import ServiceList from "./pages/ServiceList";
import Timeslotbooking from "./pages/Timeslotbooking";

const App = () => {
  return (
    <Router>  {/* This ensures that useNavigate() works */}
      <Routes>
        <Route path="/" element={<LoginSignup />} />
        <Route path="/services" element={<ServiceList />} />
        <Route path="/services/:id/timeslots" element={<Timeslotbooking/>} />
      </Routes>
    </Router>
  );
};

export default App;
