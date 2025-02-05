import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoutesCustomer = ({ allowedTypes }) => {
    // Retrieve the customer type from localStorage
    const customerType = JSON.parse(localStorage.getItem("User_Type"))
    console.log(customerType)
    // Check if the user has permission
    const isAllowed = allowedTypes.includes(customerType);

    return isAllowed ? <Outlet /> : <Navigate to="/unauthorized" replace />;
};

export default ProtectedRoutesCustomer;
