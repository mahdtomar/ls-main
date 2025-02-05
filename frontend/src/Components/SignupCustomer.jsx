import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate

export default function SignupCustomer() {
  const navigate = useNavigate(); // Initialize navigate function

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    street_name: "",
    house_number: "",
    city: "",
    zip_code: "",
    password: "",
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/customer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        alert("Customer registered successfully! Please log in.");
        navigate("/customer/login"); // Navigate to login page
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while registering. Please try again.");
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow" style={{ width: "400px" }}>
        <h2 className="text-center mb-4">Customer Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="first_name" className="form-label">
              First Name
            </label>
            <input
              type="text"
              className="form-control"
              id="first_name"
              placeholder="Enter your first name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="last_name" className="form-label">
              Last Name
            </label>
            <input
              type="text"
              className="form-control"
              id="last_name"
              placeholder="Enter your last name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="street_name" className="form-label">
              Street Name
            </label>
            <input
              type="text"
              className="form-control"
              id="street_name"
              placeholder="Enter your street name"
              value={formData.street_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="house_number" className="form-label">
              House Number
            </label>
            <input
              type="text"
              className="form-control"
              id="house_number"
              placeholder="Enter your house number"
              value={formData.house_number}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="city" className="form-label">
              City
            </label>
            <input
              type="text"
              className="form-control"
              id="city"
              placeholder="Enter your city"
              value={formData.city}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="zip_code" className="form-label">
              Zip Code
            </label>
            <input
              type="text"
              className="form-control"
              id="zip_code"
              placeholder="Enter your zip code"
              value={formData.zip_code}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              id="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary w-100">
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
}
