import React, { useEffect, useState } from 'react'
import RestaurantMenuItem from './RestaurantMenuItem'
import OrderLine from '../customer/OrderLine'

const RestaurantDashboard = () => {
    const [menu, setMenu] = useState([])
    const getRestaurantMenu = async () => {
        const res = await fetch("http://localhost:5000/restaurant/1/menu", { method: "GET" })
        const data = await res.json()
        console.log(data)
        setMenu(data)
    }
    const getRestaurantOrders = async () => {
        const res = await fetch("http://localhost:5000/restaurant/orders", { method: "GET" })
        const orders = await res.json()
        console.log("orders:", orders)
    }
    const orders = [
        {
            "order_id": 1,
            "restaurant_id": 1,
            "status": "done",
            "timestamp": '12-11-2024',
            "items": [
                { "name": "chicken alfredo", "price": 50, "quantity": 1 }
            ],
        }]
    useEffect(() => {
        getRestaurantMenu()
        getRestaurantOrders()
    }, [])
    return (
        <div>
            <div>
                order management
            </div>
            <div>
                <h2>restaurant menu</h2>
                <div className="flex-vertical">
                    {menu.map(({ id, name, description, price }, i) => {
                        return <RestaurantMenuItem key={i} id={id} name={name} description={description} price={price} />
                    })}
                </div>
            </div>
            <h2>restaurant orders</h2>
            <div>
                {orders.map(({ id, restaurant_id, status, timestamp, items }, i) => {
                    return <OrderLine key={i} id={id} restaurant_id={restaurant_id} status={status} timestamp={timestamp} items={items} />
                })}
            </div>
            <div>
                {/* restaurant balance */}
                {/*  /wallet/restaurant/:restaurant_id */}

            </div>
            <button>delete</button>
        </div>
    )
}

export default RestaurantDashboard