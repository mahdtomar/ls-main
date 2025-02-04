import React from 'react'

const CustomerOrderLine = ({ id, restaurant_id, status, timestamp, items }) => {
    return (
        <div className='flex'>
            <span>{id}</span>
            <span>{restaurant_id}</span>
            <span>{status}</span>
            <span>{timestamp}</span>
        </div>
    )
}

export default CustomerOrderLine