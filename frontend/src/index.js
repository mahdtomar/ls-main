import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "jquery/dist/jquery.min.js";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./index.css";
import { BrowserRouter } from "react-router-dom";
import { CartProvider } from "./Components/context/CartContext";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <BrowserRouter>
        <CartProvider>
            <App />
        </CartProvider>
    </BrowserRouter>
);
