import React from 'react'
import CustomerRoutes from '../routes/CustomerRoutes'
import CustomerNavbar from '../Components/misc/CustomerNavbar'

const Customer = () => {
    return (
        <div>
            <CustomerNavbar />
            <CustomerRoutes />
        </div>
    )
}

export default Customer