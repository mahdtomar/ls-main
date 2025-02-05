import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import MenuItem from './MenuItem';
import { useCart } from '../context/CartContext';
const CustomerRestaurantMenu = () => {
  const { id } = useParams()
  const [menu, setMenu] = useState([]);
  const { addToCart } = useCart()
  const getRestaurantMenu = async () => {
    try {
      const res = await fetch(`http://localhost:5000/restaurant/${id}/menu`, { method: "GET" })
      const data = await res.json()
      console.log(data)
      setMenu(data)
    } catch (error) { console.log(error) }
  }
  useEffect(() => {
    getRestaurantMenu()
  }, [])
  return (
    <div>
      <h2>Restarurant Menu</h2>
      {menu.map(({ id, name, description, price }, i) => {
        return <MenuItem key={i} id={id} name={name} description={description} price={price} />
      })}
    </div>
  )
}

export default CustomerRestaurantMenu