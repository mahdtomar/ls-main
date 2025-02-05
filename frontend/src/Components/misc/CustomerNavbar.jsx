import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import cartIcon from './../../assets/icons/ShoppingCart.svg'
import notificationsIcon from './../../assets/icons/BookmarksSimple.svg'
import './scss/navbar.css'
function CustomerNavbar() {
    const navigate = useNavigate()
    const [inputValue, setInputValue] = useState("");
    const [restaurants, setRestaurants] = useState([
        { id: 1, title: "Pizza Palace", zip_code: 123467 },
        { id: 2, title: "Sushi World", zip_code: 123499 },
        { id: 3, title: "Burger Haven", zip_code: 123444 },
        { id: 4, title: "Pasta Paradise", zip_code: 123466 }
    ])
    const [matchingRestaurants, setMatchingRestaurants] = useState([]);
    const [showNotifications, setShowNotifications] = useState(false)
    const [showCart, setShowCart] = useState(false)
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
    const user = { zip_code: 123 }
    const searchRestaurants = (value) => {
        const filtered = restaurants.filter(restaurant =>
            String(restaurant.zip_code).includes(value.toLowerCase())
        );
        setMatchingRestaurants(filtered);
    };

    const getAvailableRestaurants = async () => {
        // setRestaurants()
        try {
            const res = await fetch(`http://localhost:5000/restaurants/zip_code?zip_code=${user.zip_code}`, {
                method: "GET",
                credentials: "include",
            });
            const data = res.json()
            setRestaurants(data)
        } catch (err) { console.log(err) }
    }

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

    const getCartItems = async () => {
        try {
            const res = await fetch(`http://localhost:5000/cart/${localStorage.getItem("Customer_ID")}`)
            const cartItems = res.json()
            console.log("cart Items:", cartItems)
            setCart(cartItems)
        } catch (error) { console.log(error) }
    }
    const chooseRestaurant = (id) => {
        navigate(`/restaurant/${id}/menu`)
        setInputValue("")
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
    console.log(userType)
    return (
        <>
            {userType === "Customer" && <nav >
                <div className="container flex">
                    <div className="flex">
                        <div className="logo">Lieferspatz</div>
                        <ul className="flex">
                            <Link to={'/customer-dashboard'}>Home</Link>
                            <Link to={'/customer-orders'}>My Orders</Link>
                        </ul>
                    </div>
                    <div className="flex">
                        <div className="cart">
                            <img src={cartIcon} alt="" onClick={() => { setShowCart(curr => !curr) }} />
                            {showCart && <ul className="flex-vertical" >
                                {cart.map(({ item_id, name, price, quantity }) => <li key={item_id}>
                                    <span>{name}</span> <span>{price}</span> <span>{quantity}</span>  <span>{price * quantity}</span>
                                </li>)}
                            </ul>}
                        </div>
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
                        <div className="search">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={(e) => {
                                    setInputValue(e.target.value);
                                    searchRestaurants(e.target.value);
                                }}
                                placeholder="Search restaurants by ZIP code..."
                            />
                            {matchingRestaurants.length > 0 && inputValue !== "" && (
                                <ul className="search-results">
                                    {matchingRestaurants.map((restaurant) => (
                                        <li key={restaurant.id} onClick={() => { chooseRestaurant(restaurant.id) }}>{restaurant.title}</li>
                                    ))}
                                </ul>
                            )}
                        </div>
                        <button className="btn btn-danger" onClick={handleLogout}>Logout</button>
                    </div>
                </div>
            </nav>}
        </>
    );
}

export default CustomerNavbar;
