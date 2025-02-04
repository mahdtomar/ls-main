import React from "react";
import { Link } from "react-router-dom";

export default function Login() {
  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="text-center">
        <h2 className="mb-4">Login</h2>
        <div className="d-grid gap-3">
          {/* Link for Customer Login */}
          <Link to="/customer/login" className="btn btn-primary btn-lg">
            Login as Customer
          </Link>

          {/* Link for Restaurant Owner Login */}
          <Link to="/restaurant/login" className="btn btn-secondary btn-lg">
            Login as Restaurant Owner
          </Link>
        </div>
      </div>
    </div>
  );
}
