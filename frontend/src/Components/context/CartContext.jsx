import { createContext, useContext, useEffect, useState } from "react";

// Create the Context
const CartContext = createContext();

// Custom hook for easier access
export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
    const [cart, setCart] = useState([
        { 'item_id': 123, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
        { 'item_id': 12343, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
        { 'item_id': 1243, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
        { 'item_id': 1523, 'name': ' item[1]', 'price': 55, 'quantity': 2 },
    ]);
    const getCartItems = async () => {
        try {
            const res = await fetch(`http://localhost:5001/cart/${localStorage.getItem("Customer_ID")}`)
            const cartItems = res.json()
            console.log("cart Items:", cartItems)
            setCart(cartItems)
        } catch (error) { console.log(error) }
    }
    // Add item to cart
    const addToCart = (product) => {
        setCart((prevCart) => {
            const existingItem = prevCart.find((item) => item.id === product.id);

            if (existingItem) {
                return prevCart.map((item) =>
                    item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
                );
            } else {
                return [...prevCart, { ...product, quantity: 1 }];
            }
        });
    };

    // Remove item from cart
    const removeFromCart = (id) => {
        setCart((prevCart) => prevCart.filter((item) => item.id !== id));
    };

    // Update quantity
    const updateQuantity = (id, quantity) => {
        setCart((prevCart) =>
            prevCart.map((item) =>
                item.id === id ? { ...item, quantity: quantity } : item
            )
        );
    };

    // Clear cart
    const clearCart = () => setCart([]);

    // Get cart total price
    const getTotalPrice = () => {
        return cart.reduce((total, item) => total + item.price * item.quantity, 0);
    };
    // useEffect(()=>{getCartItems();},[])
    return (
        <CartContext.Provider
            value={{ cart, addToCart, removeFromCart, updateQuantity, clearCart, getTotalPrice }}
        >
            {children}
        </CartContext.Provider>
    );
};
