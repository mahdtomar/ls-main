import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div
      className="d-flex justify-content-center align-items-center vh-100"
      style={{
        backgroundColor: "white",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        className="d-flex flex-column align-items-center"
        style={{ position: "relative", zIndex: 1 }}
      >
        {/* Welcome message */}
        <h1
          className="mb-4"
          style={{ fontSize: "2rem", fontWeight: "bold", color: "#343a40" }}
        >
          Welcome to Lieferspatz
        </h1>

        {/* Login Button */}
        <Link
          className="btn btn-primary mb-3"
          to="/login"
          style={{
            fontSize: "1.25rem",
            padding: "0.75rem 2rem",
            borderRadius: "8px",
            transition: "background-color 0.3s ease, transform 0.2s ease",
            width: "200px",
            textAlign: "center",
          }}
          onMouseEnter={(e) => (e.target.style.backgroundColor = "#0056b3")}
          onMouseLeave={(e) => (e.target.style.backgroundColor = "#007bff")}
        >
          Login
        </Link>

        {/* Sign Up Button */}
        <Link
          to="/signup"
          className="btn btn-secondary"
          style={{
            fontSize: "1.25rem",
            padding: "0.75rem 2rem",
            borderRadius: "8px",
            transition: "background-color 0.3s ease, transform 0.2s ease",
            width: "200px",
            textAlign: "center",
          }}
          onMouseEnter={(e) => (e.target.style.backgroundColor = "#545b62")}
          onMouseLeave={(e) => (e.target.style.backgroundColor = "#6c757d")}
        >
          Sign Up
        </Link>
      </div>
    </div>
  );
}
