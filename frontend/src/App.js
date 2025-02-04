import "./App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "./Components/Navbar";
import Home from "./Components/Home";
import Login from "./Components/Login";
import LoginCustomer from "./Components/LoginCustomer";
import LoginRestaurant from "./Components/LoginRestaurant";

import Signup from "./Components/Signup";
import SignupCustomer from "./Components/SignupCustomer";
import SignupRestaurant from "./Components/SignupRestaurant";
import CustomerDashboard from "./Components/CustomerDashboard";

function App() {
    return (
        <>
            <Navbar />
            <Routes>
                <Route path="" element={<Home />} />
                <Route path="login" element={<Login />} />
                <Route path="customer/login" element={<LoginCustomer />} />
                <Route path="/restaurant/login" element={<LoginRestaurant />} />

                <Route path="signup" element={<Signup />} />
                <Route path="customer" element={<SignupCustomer />} />
                <Route path="restaurant" element={<SignupRestaurant />} />
                <Route
                    path="customer-dashboard"
                    element={<CustomerDashboard />}
                />
            </Routes>
        </>
    );
}

export default App;
