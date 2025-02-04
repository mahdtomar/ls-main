import React from 'react'
import RestaurantRoutes from '../routes/RestaurantRoutes'
import RestaurantNavbar from '../Components/misc/RestaurantNavbar'

const Restaurant = () => {
    return (
        <div>
            <RestaurantNavbar />
            <RestaurantRoutes />
        </div>
    )
}

export default Restaurant