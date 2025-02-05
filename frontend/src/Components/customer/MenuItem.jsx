import React from 'react'
import { useCart } from '../context/CartContext'

const MenuItem = ({ id, name, description, price }) => {
  const { addToCart } = useCart()
  return (
    <div className='container flex-vertical'>
      <div className='flex'>
        <span>{id}</span>
        <span>{name}</span>
        <span>{description}</span>
        <span>{price}</span>
        <button className='btn btn-success' onClick={() => { addToCart({ id, name, description, price }) }}>Add To Cart</button>
      </div>
    </div>
  )
}

export default MenuItem