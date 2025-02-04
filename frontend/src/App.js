// import LoginRestaurant from "./Components/LoginRestaurant";
// import RestaurantRoutes from "./routes/RestaurantRoutes";
// import SignupCustomer from "./Components/SignupCustomer";
// import LoginCustomer from "./Components/LoginCustomer";
// import CustomerDashboard from "./Components/customer/CustomerDashboard";
// import Navbar from "./Components/Navbar";
// import RestaurantDashboard from "./Components/restaurant/RestaurantDashboard";
// import CustomerRoutes from "./routes/CustomerRoutes";
// import SignupRestaurant from "./Components/SignupRestaurant";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import Home from "./Components/Home";
import Login from "./Components/Login";
import Signup from "./Components/Signup";
import CustomerNavbar from "./Components/misc/CustomerNavbar";
import Customer from "./Pages/Customer";
import Restaurant from "./Pages/Restaurant";

function App() {
    return (
        <>
            {/* <Navbar /> */}
            <Routes>
                <Route path="" element={<Home />} />
                <Route path="login" element={<Login />} />
                <Route path="signup" element={<Signup />} />
            </Routes>
            <Customer />
            <Restaurant />
        </>
    );
}

export default App;
