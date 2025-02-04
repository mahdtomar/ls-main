import React from 'react'
import { Route, Routes } from 'react-router-dom'
import CustomerDashboard from '../Components/customer/CustomerDashboard'
import SignupCustomer from '../Components/SignupCustomer'
import LoginCustomer from '../Components/LoginCustomer'

const CustomerRoutes = () => {
    return (
        <Routes>
            <Route path="customer/login" element={<LoginCustomer />} />
            <Route path="customer" element={<SignupCustomer />} />
            <Route
                path="customer-dashboard"
                element={<CustomerDashboard />}
            />
        </Routes>
    )
}

export default CustomerRoutes;