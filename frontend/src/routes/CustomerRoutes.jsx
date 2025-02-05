import React from 'react'
import { Route, Routes } from 'react-router-dom'
import CustomerDashboard from '../Components/customer/CustomerDashboard'
import SignupCustomer from '../Components/SignupCustomer'
import LoginCustomer from '../Components/LoginCustomer'
import RestaurantMenu from '../Components/restaurant/RestaurantMenu'
import CustomerOrders from '../Components/customer/CustomerOrders'
import ProtectedRoutesCustomer from './ProtectedRoutesCustomer'

const CustomerRoutes = () => {
    return (
        <Routes>
            <Route element={<ProtectedRoutesCustomer allowedTypes={["Customer"]} />}>
                <Route
                    path="/customer-dashboard"
                    element={<CustomerDashboard />}
                />
                <Route path='/customer-orders' element={<CustomerOrders />} />
            </Route>
            <Route path="/customer/login" element={<LoginCustomer />} />
            <Route path="/customer" element={<SignupCustomer />} />
            <Route path='/restaurant/:id/menu' element={<RestaurantMenu />} />
        </Routes>
    )
}

export default CustomerRoutes;