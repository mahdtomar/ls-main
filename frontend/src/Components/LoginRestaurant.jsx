import React from "react";

export default function LoginRestaurant() {
  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow" style={{ width: "400px" }}>
        <h2 className="text-center mb-4">Restaurant Login</h2>
        <form>
          {/* Restaurant Name */}
          <div className="mb-3">
            <label htmlFor="name" className="form-label">
              Restaurant Name
            </label>
            <input
              type="text"
              className="form-control"
              id="name"
              placeholder="Enter restaurant name"
            />
          </div>

          {/* Password */}
          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              id="password"
              placeholder="Enter your password"
            />
          </div>

          {/* Submit Button */}
          <button type="submit" className="btn btn-primary w-100">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
