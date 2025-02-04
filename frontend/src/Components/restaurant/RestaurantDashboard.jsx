import React, { useEffect, useState } from 'react'
import RestaurantMenuItem from './RestaurantMenuItem'

const RestaurantDashboard = () => {
    const [menu, setMenu] = useState([])
    const getRestaurantMenu = async () => {
        const res = await fetch("http://localhost:5000/restaurant/1/menu", { method: "GET" })
        const data = await res.json()
        console.log(data)
        setMenu(data)
    }
    useEffect(() => {
        getRestaurantMenu()
    })
    const restaurantMenu = [{
        "id": 1,
        "name": "menu item 1",
        "description": 'brief description',
        "price": 100,
    }]
    return (
        <div>
            <div>
                order management
            </div>
            <div>
                <div className="flex-vertical">
                    {menu.map(({ id, name, description, price }, i) => {
                        return <RestaurantMenuItem id={id} name={name} description={description} price={price} />
                    })}
                </div>
            </div>
            <div>
                order history
            </div>
            <div>
                restaurant balance
            </div>
            <button>delete</button>
        </div>
    )
}

export default RestaurantDashboard