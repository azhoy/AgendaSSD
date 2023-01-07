import React, {useContext} from 'react'
import {Link} from 'react-router-dom'
import AuthContext from "../context/AuthContext";

const Header = () => {
    // @ts-ignore
    let {user, logoutUser} = useContext(AuthContext)
    return (
        <div>
            <Link to='/'>Home</Link>
            <span>   |   </span>
            <Link to='/contacts'>Contacts</Link>
            {
                user ? (<p onClick={logoutUser}>Logout</p>):(
                    <div>
                        <Link to='/login'>Login</Link>
                        <span>   |   </span>
                        <Link to='/register'>Register</Link>
                    </div>
                )
            }
            {user && <p> Hello {user.username}</p> }
        </div>
    )
}

export default Header