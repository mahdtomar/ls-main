import React, { useState } from 'react'

const MenuItemForm = ({ itemName, itemDescription, itemPrice, id, setShowMenuForm }) => {
    const [name, setName] = useState(itemName);
    const [description, setDescription] = useState(itemDescription);
    const [price, setPrice] = useState(itemPrice);
    const handleSubmit = async () => {
        console.log({ name, description, price, id })
    }
    const closeWindow = () => {
        setShowMenuForm(false)
    }
    return (
        <div className="form">
            <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder='item name' />
            <input type="text" value={description} onChange={e => setDescription(e.target.value)} placeholder='description' />
            <input type="number" value={price} onChange={e => setPrice(e.target.value)} placeholder='price' />
            <button onClick={handleSubmit} className='btn btn-success'>Save</button>
            <span onClick={closeWindow} className='btn btn-danger'>Close</span>
        </div>
    )
}

export default MenuItemForm