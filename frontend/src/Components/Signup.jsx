import React from "react";
import { Link } from "react-router-dom";

export default function Signup() {
  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="text-center">
        <h2 className="mb-4">Sign Up</h2>
        <div className="d-grid gap-3">
          <Link
            to="/customer"
            className="btn btn-primary btn-lg"
            style={{
              transition: "background-color 0.3s ease, transform 0.2s ease",
            }}
            onMouseEnter={(e) => (e.target.style.backgroundColor = "#0056b3")}
            onMouseLeave={(e) => (e.target.style.backgroundColor = "#007bff")}
          >
            Sign Up as Customer
          </Link>

          <Link
            to="/restaurant"
            className="btn btn-secondary btn-lg"
            style={{
              transition: "background-color 0.3s ease, transform 0.2s ease",
            }}
            onMouseEnter={(e) => (e.target.style.backgroundColor = "#545b62")}
            onMouseLeave={(e) => (e.target.style.backgroundColor = "#6c757d")}
          >
            Sign Up as Restaurant Owner
          </Link>
        </div>
      </div>
    </div>
  );
}
