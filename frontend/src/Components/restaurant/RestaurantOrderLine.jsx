import React from 'react'

const RestaurantOrderLine = ({ id, restaurant_id, status, timestamp, items }) => {
    return (
        <div className='flex'>
            <span>{id}</span>
            <span>{restaurant_id}</span>
            <span>{status}</span>
            <span>{timestamp}</span>
            <span className="flex">
                <button className="accept btn btn-primary">Accept</button>
                <button className='decline btn btn-danger'>Decline</button>
            </span>
        </div>
    )
}

export default RestaurantOrderLine