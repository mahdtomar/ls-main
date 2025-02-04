import React from 'react'
import { Route, Routes } from 'react-router-dom'
import RestaurantDashboard from '../Components/restaurant/RestaurantDashboard'
import LoginRestaurant from '../Components/LoginRestaurant'
import SignupRestaurant from '../Components/SignupRestaurant'
import RestaurantMenu from '../Components/restaurant/RestaurantMenu'

const RestaurantRoutes = () => {
    return (
        <Routes>
            <Route path="restaurant" element={<SignupRestaurant />} />
            <Route path="/restaurant/login" element={<LoginRestaurant />} />
            <Route
                path="/restaurant-dashboard"
                element={<RestaurantDashboard />}
            />
            <Route path='/restaurant-menu' element={<RestaurantMenu />} />
        </Routes>
    )
}

export default RestaurantRoutes