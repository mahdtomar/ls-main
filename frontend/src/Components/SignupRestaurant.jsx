import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import axios from "axios";

export default function SignupRestaurant() {
  const navigate = useNavigate(); // Initialize navigate function

  const [formData, setFormData] = useState({
    name: "",
    street_name: "",
    house_number: "",
    city: "",
    zip_code: "",
    description: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/restaurant", formData);
      alert("Restaurant registered successfully! Please log in.");
      navigate("/restaurant/login"); // Navigate to login page
    } catch (error) {
      alert("Error: " + (error.response?.data?.error || error.message));
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow" style={{ width: "400px" }}>
        <h2 className="text-center mb-4">Restaurant Sign Up</h2>
        <form onSubmit={handleSubmit}>
          {/* Restaurant Name */}
          <div className="mb-3">
            <label htmlFor="name" className="form-label">
              Restaurant Name
            </label>
            <input
              type="text"
              className="form-control"
              id="name"
              name="name"
              placeholder="Enter your restaurant name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          {/* Street Name */}
          <div className="mb-3">
            <label htmlFor="street_name" className="form-label">
              Street Name
            </label>
            <input
              type="text"
              className="form-control"
              id="street_name"
              name="street_name"
              placeholder="Enter your street name"
              value={formData.street_name}
              onChange={handleChange}
              required
            />
          </div>

          {/* House Number */}
          <div className="mb-3">
            <label htmlFor="house_number" className="form-label">
              House Number
            </label>
            <input
              type="text"
              className="form-control"
              id="house_number"
              name="house_number"
              placeholder="Enter your house number"
              value={formData.house_number}
              onChange={handleChange}
              required
            />
          </div>

          {/* City */}
          <div className="mb-3">
            <label htmlFor="city" className="form-label">
              City
            </label>
            <input
              type="text"
              className="form-control"
              id="city"
              name="city"
              placeholder="Enter your city"
              value={formData.city}
              onChange={handleChange}
              required
            />
          </div>

          {/* Zip Code */}
          <div className="mb-3">
            <label htmlFor="zip_code" className="form-label">
              Zip Code
            </label>
            <input
              type="text"
              className="form-control"
              id="zip_code"
              name="zip_code"
              placeholder="Enter your zip code"
              value={formData.zip_code}
              onChange={handleChange}
              required
            />
          </div>

          {/* Description */}
          <div className="mb-3">
            <label htmlFor="description" className="form-label">
              Description
            </label>
            <textarea
              className="form-control"
              id="description"
              name="description"
              placeholder="Enter a brief description"
              value={formData.description}
              onChange={handleChange}
              required
            ></textarea>
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
              name="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          {/* Submit Button */}
          <button type="submit" className="btn btn-primary w-100">
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
}
