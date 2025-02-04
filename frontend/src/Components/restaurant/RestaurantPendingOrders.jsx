import React from 'react'
import RestaurantOrderLine from './RestaurantOrderLine'


const RestaurantPendingOrders = () => {
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
    return (
        <div>
            <h2>RestaurantPendingOrders</h2>
            {orders.map(({ id, restaurant_id, status, timestamp, items }, i) => {
                return <RestaurantOrderLine key={i} id={id} restaurant_id={restaurant_id} status={status} timestamp={timestamp} items={items} />
            })}
        </div>
    )
}

export default RestaurantPendingOrders