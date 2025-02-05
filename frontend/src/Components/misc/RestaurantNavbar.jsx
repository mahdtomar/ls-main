import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import cartIcon from './../../assets/icons/ShoppingCart.svg'
import notificationsIcon from './../../assets/icons/BookmarksSimple.svg'

const RestaurantNavbar = () => {
    const [showNotifications, setShowNotifications] = useState(false)
    const [showCart, setShowCart] = useState(false)
    const navigate = useNavigate()
    const [notifications, setNotifications] = useState(
        [
            { "id": 1, "message": "notifications message 1", "timestamp": "12-11-2025" },
            { "id": 2, "message": "notifications message 1", "timestamp": "12-11-2025" },
            { "id": 3, "message": "notifications message 1", "timestamp": "12-11-2025" },
        ]
    )
    const [cart, setCart] = useState(
        [
            { 'item_id': 123, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
            { 'item_id': 12343, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
            { 'item_id': 1243, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
            { 'item_id': 1523, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
        ])
    const getCustomerNotification = async () => {
        try {
            const res = await fetch(`http://localhost:5000/notifications/${localStorage.getItem("Customer_ID")}`, { method: "GET", credentials: "include" })
            const data = await res.json()
            console.log("customer notifications : ", data)
            setNotifications(data)
        } catch (error) {
            console.log(error)
        }
    }
    const handleLogout = async () => {
        try {
            const res = await fetch("http://localhost:5000/logout", { method: "POST", credentials: "include" })
            const data = await res.json()
            if (res.ok) {
                navigate("/")
            }
            console.log(data)

        } catch (err) { console.log("error loggging out", err) }
    }
    const getCartItems = async () => {
        try {
            const res = await fetch(`http://localhost:5000/cart/${localStorage.getItem("Customer_ID")}`)
            const cartItems = res.json()
            console.log("cart Items:", cartItems)
            setCart(cartItems)
        } catch (error) { console.log(error) }
    }
    useEffect(() => {
        // getAvailableRestaurants();
        // getCustomerNotification();
        // const callingNotifications = setInterval(() => {
        //     getCustomerNotification();
        //     getCartItems();
        //     console.log(notifications)
        // }, (5000));
        // return () => clearInterval(callingNotifications)
    }, [])
    const userType = JSON.parse(localStorage.getItem("User_Type"))
    return (
        <>
            {userType === "Restaurant" && <nav >
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
                        <div className="notifications"><img src={notificationsIcon} alt="" onClick={() => { setShowNotifications(curr => !curr) }} />
                            {showNotifications && <ul className="flex-vertical">
                                {notifications.map(({ message, id, timestamp }) => <li key={id}>
                                    <span>{message}</span>
                                    <span>{timestamp}</span>
                                </li>)}</ul>}
                        </div>
                        <div className="balance">
                            {/* not working yet */}
                            $0
                        </div>
                        <button className="btn btn-danger" onClick={handleLogout}>Logout</button>

                    </div>
                </div>
            </nav>}
        </>
    )
}

export default RestaurantNavbar