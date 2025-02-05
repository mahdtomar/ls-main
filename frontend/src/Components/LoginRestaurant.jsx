import React from "react";
import { useNavigate } from "react-router-dom";

export default function LoginRestaurant() {
  const navigate = useNavigate()
  const handleSubmit = async () => {
    try {
      const res = await fetch("http://localhost:5001/restaurant/login", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({})
      })
      const data = res.json()
      localStorage.setItem("User_Type", JSON.stringify("Restaurant"))

      if (res.ok) {
        navigate("/restaurant-dashboard")
      }
      console.log(data)
    } catch (error) { console.log("error") }
  }
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
          <button type="submit" className="btn btn-primary w-100" onClick={handleSubmit}>
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
