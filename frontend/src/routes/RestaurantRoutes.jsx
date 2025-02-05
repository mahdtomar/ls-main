import React from 'react'
import { Route, Routes } from 'react-router-dom'
import RestaurantDashboard from '../Components/restaurant/RestaurantDashboard'
import LoginRestaurant from '../Components/LoginRestaurant'
import SignupRestaurant from '../Components/SignupRestaurant'
import RestaurantMenu from '../Components/restaurant/RestaurantMenu'
import RestaurantPendingOrders from '../Components/restaurant/RestaurantPendingOrders'
import RestaurantOrderHistory from '../Components/restaurant/RestaurantOrderHistory'
import ProtectedRoutesCustomer from './ProtectedRoutesCustomer'

const RestaurantRoutes = () => {
    return (
        <Routes>
            <Route element={<ProtectedRoutesCustomer allowedTypes={["Restaurant"]} />}>
                <Route path="/restaurant-dashboard" element={<RestaurantDashboard />} />
                <Route path='/restaurant-menu' element={<RestaurantMenu />} />
                <Route path='/restaurant-orders' element={<RestaurantPendingOrders />} />
                <Route path='/restaurant-orders-history' element={<RestaurantOrderHistory />} />
            </Route>
            <Route path="restaurant" element={<SignupRestaurant />} />
            <Route path="/restaurant/login" element={<LoginRestaurant />} />
        </Routes>
    )
}

export default RestaurantRoutes