import React from "react";

const CustomerDashboard = () => {
  return (
    <div className="container my-4">
      <div className="card">
        <div className="card-header bg-primary text-white">
          <h4>Customer Dashboard</h4>
        </div>
        <div className="card-body">
          {/* My Orders Section */}
          <div className="mb-4">
            <h5 className="text-success">✔ My Orders</h5>
            <p>List of past & active orders (Order ID, Status, Timestamp)</p>
          </div>

          {/* My Data Section */}
          <div className="mb-4">
            <h5 className="text-success">✔ My Data</h5>
            <p>Personal details (Name, Address, ZIP Code)</p>
          </div>

          {/* Customer Balance Section */}
          <div className="mb-4">
            <h5 className="text-success">✔ Customer Balance</h5>
            <p>Shows current wallet balance</p>
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
