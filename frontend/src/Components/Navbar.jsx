import React from "react";
import { Link } from "react-router-dom";
function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
      <div className="container">
        {/* Brand Name */}
        <Link className="navbar-brand" to="/">
          LieferSpatz
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
