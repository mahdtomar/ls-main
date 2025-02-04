import React from 'react'

const RestaurantMenuItem = ({ id, name, description, price }) => {
    return (
        <div className='flex'>
            <span>{id}</span>
            <span>{name}</span>
            <span>{description}</span>
            <span>{price}</span>
        </div>
    )
}

export default RestaurantMenuItem