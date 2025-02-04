import React from 'react'
import { Link } from 'react-router-dom'

const RestaurantNavbar = () => {
    return (
        <nav >
            <div className="container flex">
                <div className="flex">
                    <div className="logo">Lieferspatz</div>
                    <ul className="flex">
                        <Link to={'/restaurant-dashboard'}>Home</Link>
                        <Link to={'/restaurant-orders'}>Orders</Link>
                        <Link to={'/restaurant-menu'}>Menu</Link>
                        <Link to={`/restaurant-orders-history`}>Order History</Link>
                    </ul>
                </div>
                <div className="flex">
                    <div className="balance">
                        {/* not working yet */}
                        $0
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default RestaurantNavbar