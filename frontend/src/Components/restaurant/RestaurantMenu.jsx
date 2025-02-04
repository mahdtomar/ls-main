import React, { useEffect, useState } from 'react'
import RestaurantMenuItem from './RestaurantMenuItem'
import MenuItemForm from './MenuItemForm';

const RestaurantMenu = () => {
    const [menu, setMenu] = useState([]);
    const [item, setItem] = useState({})
    const [showMenuForm, setShowMenuForm] = useState(false)
    const getRestaurantMenu = async () => {
        const res = await fetch("http://localhost:5000/restaurant/1/menu", { method: "GET" })
        const data = await res.json()
        console.log(data)
        setMenu(data)
    }

    useEffect(() => {
        getRestaurantMenu();
    }, [])
    return (
        <div className='restaurantMenu'>
            <h2>restaurant menu</h2>
            <div className="flex-vertical">
                {menu.map(({ id, name, description, price }, i) => {
                    return <RestaurantMenuItem key={i} id={id} name={name} description={description} price={price} setItem={setItem} setShowMenuForm={setShowMenuForm} />
                })}
            </div>
            {showMenuForm && <MenuItemForm itemName={item.name} itemDescription={item.description} itemPrice={item.price} id={item.id} setShowMenuForm={setShowMenuForm} />}
        </div>
    )
}

export default RestaurantMenu