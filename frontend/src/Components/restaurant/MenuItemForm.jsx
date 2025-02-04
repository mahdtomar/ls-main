import React, { useState } from 'react'
import './scss/menuitemform.css'
const MenuItemForm = ({ itemName, itemDescription, itemPrice, id, setShowMenuForm }) => {
    const [name, setName] = useState(itemName);
    const [description, setDescription] = useState(itemDescription);
    const [price, setPrice] = useState(itemPrice);
    const handleSubmit = async () => {
        if (id === "new") {
            console.log("create new item")
        } else {
            console.log("update current item")
        }
    }
    const closeWindow = () => {
        setShowMenuForm(false)
    }
    return (
        <div className="menu-item-form ">
            <div className="copntainer flex-vertical">
                <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder='item name' />
                <input type="text" value={description} onChange={e => setDescription(e.target.value)} placeholder='description' />
                <input type="number" value={price} onChange={e => setPrice(e.target.value)} placeholder='price' />
                <button onClick={handleSubmit} className='btn btn-success'>Save</button>
                <span onClick={closeWindow} className='btn btn-danger'>Close</span>
            </div>
        </div>
    )
}

export default MenuItemForm