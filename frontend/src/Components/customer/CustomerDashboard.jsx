import React, { useEffect } from "react";
import CustomerOrderLine from "./OrderLine";
import { useNavigate } from "react-router-dom";

const CustomerDashboard = () => {
  const navigate = useNavigate()
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
  const userData = {
    'first_name': "omar",
    'last_name': "mahdy",
    'street_name': "street1",
    'house_number': "132",
    'city': "tanta",
    'zip_code': "123456"
  }
  const getCustomerOrders = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/orders/history/1", {
        method: "GET",
        credentials: "include"
      })
      console.log(res)
      const orders = await res.json()
      console.log(orders)
    } catch (error) { console.log(error) }
  }
  const getWalletBalance = async () => {
    try {
      const res = await fetch(`http://localhost:5001/wallet/customer/${localStorage.getItem("Customer_ID")}`, { method: "GET", credentials: "include" })
      const data = await res.json()
      console.log(data)
    } catch (error) { console.log(error) }
  }

  const getUserProfile = async () => {
    try {
      const res = await fetch("http://localhost:5001/customer/3/profile", { credentials: "include", method: "GET" })
      const data = await res.json()
      console.log("user profile", data)
    } catch (error) { console.log(error) }
  }
  const checkSession = async () => {
    try {
      const res = await fetch(`http://localhost:5001/session`, {
        method: "GET",
        credentials: "include",
      })
      const data = await res.json()
      console.log("check session", data)
    } catch (err) {
      console.log(err)
    }
  }
  const handleLogout = async () => {
    try {
      const res = await fetch("http://localhost:5001/logout", { method: "POST", credentials: "include" })
      const data = await res.json()
      if (res.ok) {
        navigate("/")
      }
      console.log(data)

    } catch (err) { console.log("error loggging out", err) }
  }
  useEffect(() => { getCustomerOrders(); getWalletBalance(); checkSession(); getUserProfile() }, [])
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
            <h5 className="text-success"> My Data</h5>
            <ul>
              <li>First Name : {userData.first_name}</li>
              <li>Last Name : {userData.last_name}</li>
              <li>Street: {userData.street_name}</li>
              <li>City : {userData.city}</li>
              <li>House Number : {userData.house_number}</li>
              <li>Zip Code : {userData.zip_code}</li>
            </ul>
          </div>

          {/* Logout Button */}
          <div>
            <button className="btn btn-danger" onClick={handleLogout}>Logout</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerDashboard;
