import { useState } from "react";
import { Link } from "react-router-dom";
import './scss/navbar.css'
function CustomerNavbar() {
    const [inputValue, setInputValue] = useState("");
    const [matchingRestaurants, setMatchingRestaurants] = useState([]);

    const restaurants = [
        { id: 1, title: "Pizza Palace", zip_code: 123467 },
        { id: 2, title: "Sushi World", zip_code: 123499 },
        { id: 3, title: "Burger Haven", zip_code: 123444 },
        { id: 4, title: "Pasta Paradise", zip_code: 123466 }
    ];
    const searchRestaurants = (value) => {
        const filtered = restaurants.filter(restaurant =>
            String(restaurant.zip_code).includes(value.toLowerCase())
        );
        setMatchingRestaurants(filtered);
    };

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
