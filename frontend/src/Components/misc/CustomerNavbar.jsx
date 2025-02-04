import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import cartIcon from './../../assets/icons/ShoppingCart.svg'
import notificationsIcon from './../../assets/icons/BookmarksSimple.svg'
import './scss/navbar.css'
function CustomerNavbar() {
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
    return (
        <nav >
            <div className="container flex">
                <div className="flex">
                    <div className="logo">Lieferspatz</div>
                    <ul className="flex">
                        <Link to={'/customer-dashboard'}>Home</Link>
                        <Link>My Orders</Link>
                    </ul>
                </div>
                <div className="flex">
                    <div className="cart"><img src={cartIcon} alt="" onClick={() => { setShowCart(curr => !curr) }} />
                        {showCart && cart.map(({ item_id, name, price, quantity }) => <div className="flex" key={item_id}>
                            <span>{name}</span> <span>{price}</span> <span>{quantity}</span>  <span>{price * quantity}</span>
                        </div>)}
                    </div>
                    <div className="notifications"><img src={notificationsIcon} alt="" onClick={() => { setShowNotifications(curr => !curr) }} />
                        {showNotifications && notifications.map(({ message, id, timestamp }) => <div key={id}>
                            <span>{message}</span>
                            <span>{timestamp}</span>
                        </div>)}
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
                    </div>
                </div>
                {matchingRestaurants.length > 0 && inputValue !== "" && (
                    <ul className="search-results">
                        {matchingRestaurants.map((restaurant) => (
                            <li key={restaurant.id}>{restaurant.title}</li>
                        ))}
                    </ul>
                )}
            </div>
        </nav>
    );
}

export default CustomerNavbar;
