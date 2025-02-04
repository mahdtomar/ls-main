import React from 'react'

const RestaurantMenuItem = ({ id, name, description, price, setItem, setShowMenuForm }) => {
    const handleEdit = () => {
        setItem({ name: name, description: description, price: price, id: id })
        setShowMenuForm(true)
    }
    return (
        <div className='flex'>
            <span>{id}</span>
            <span>{name}</span>
            <span>{description}</span>
            <span>{price}</span>
            <span className="options flex">
                <span className='edit btn btn-info' onClick={handleEdit}>Edit</span>
                <span className='delete btn btn-danger'>Delete</span>
            </span>
        </div>
    )
}

export default RestaurantMenuItem