import React, { useEffect, useState } from 'react'
import RestaurantMenuItem from './RestaurantMenuItem'
import OrderLine from '../customer/OrderLine'
import MenuItemForm from './MenuItemForm'
import RestaurantOrderLine from './RestaurantOrderLine'

const RestaurantDashboard = () => {
    const [menu, setMenu] = useState([])
    const [item, setItem] = useState({})
    const [showMenuForm, setShowMenuForm] = useState(false)

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
                pending order management
                {orders.map(({ id, restaurant_id, status, timestamp, items }, i) => {
                    return <RestaurantOrderLine key={i} id={id} restaurant_id={restaurant_id} status={status} timestamp={timestamp} items={items} />
                })}
            </div>
            <div>
                <h2>restaurant menu</h2>
                <div className="flex-vertical">
                    {menu.map(({ id, name, description, price }, i) => {
                        return <RestaurantMenuItem key={i} id={id} name={name} description={description} price={price} setItem={setItem} setShowMenuForm={setShowMenuForm} />
                    })}
                    {showMenuForm && <MenuItemForm itemName={item.name} itemDescription={item.description} itemPrice={item.price} id={item.id} setShowMenuForm={setShowMenuForm} />}

                </div>
            </div>
            <h2>restaurant orders</h2>
            <div>
                {orders.map(({ id, restaurant_id, status, timestamp, items }, i) => {
                    return <RestaurantOrderLine key={i} id={id} restaurant_id={restaurant_id} status={status} timestamp={timestamp} items={items} />
                })}
            </div>
            <div>
                {/* restaurant balance */}
                {/*  /wallet/restaurant/:restaurant_id */}

            </div>
            <button>logout</button>
        </div>
    )
}

export default RestaurantDashboard