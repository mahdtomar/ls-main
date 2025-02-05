import React from 'react'
import CustomerOrderLine from './OrderLine'

const CustomerOrders = () => {
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
    const getCustomerOrders = async () => {
        const res = await fetch("http://127.0.0.1:5000/orders/history/1", {
            method: "GET",
            credentials: "include"
        })
        console.log(res)
        const orders = await res.json()
        console.log(orders)
    }
    return (
        <div className="mb-4">
            <h5 className="text-success"> My Orders</h5>
            {orders.map(({ id, restaurant_id, status, timestamp, items }, i) => {
                return <CustomerOrderLine key={i} id={id} restaurant_id={restaurant_id} status={status} timestamp={timestamp} items={items} />
            })}
        </div>
    )
}

export default CustomerOrders