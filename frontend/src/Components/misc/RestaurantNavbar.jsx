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
                        <Link>Orders</Link>
                        <Link to={'/restaurant-menu'}>Menu</Link>
                        <Link>Order History</Link>
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