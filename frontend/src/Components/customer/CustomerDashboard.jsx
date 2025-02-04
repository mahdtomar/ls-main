import React, { useEffect } from "react";
import CustomerOrderLine from "./CustomerOrderLine";

const CustomerDashboard = () => {
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
  //   order_details = {
  //     "order_id": order[0],
  //     "customer_id": order[1],
  //     "restaurant_id": order[2],
  //     "status": order[3],
  //     "timestamp": order[4],
  //     "items": [{"name": i[0], "price": i[1], "quantity": i[2]} for i in items],
  // }
  const getCustomerOrders = async () => {
    const res = await fetch("http://127.0.0.1:5000/orders/history/1", { method: "GET" })
    console.log(res)
    const orders = await res.json()
    console.log(orders)
  }
  useEffect(() => { getCustomerOrders() }, [])
  return (
    <div className="container my-4">
      <div className="card">
        <div className="card-header bg-primary text-white">
          <h4>Customer Dashboard</h4>
        </div>
        <div className="card-body">
          {/* My Orders Section */}
          <div className="mb-4">
            <h5 className="text-success"> My Orders</h5>
            {orders.map(({ id, restaurant_id, status, timestamp, items }, i) => {
              return <CustomerOrderLine key={i} id={id} restaurant_id={restaurant_id} status={status} timestamp={timestamp} items={items} />
            })}
          </div>

          {/* My Data Section */}
          <div className="mb-4">
            <h5 className="text-success">✔ My Data</h5>
            <p>Personal details (Name, Address, ZIP Code)</p>
            {/* not available */}
          </div>

          {/* Customer Balance Section */}
          <div className="mb-4">
            <h5 className="text-success">✔ Customer Balance</h5>
            <p>Shows current wallet balance</p>
            {/* not available */}
          </div>

          {/* Logout Button */}
          <div>
            <h5 className="text-success">✔ Logout Button</h5>
            <button className="btn btn-danger">Logout</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerDashboard;
