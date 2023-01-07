import React, {useContext} from "react";
import KeyContext from "../context/KeyContext";


const RegisterPage = () => {
    let {registerUser} = useContext(KeyContext)
    return (
        <div>
            <form onSubmit={registerUser}>
                <input type="text" name="email" placeholder="Enter Email"/>
                <input type="text" name="username" placeholder="Enter Username"/>
                <input type="password" name="password" placeholder="Enter your password"/>
                <input type="password" name="re_password" placeholder="Verify your password"/>
                <input type="submit" />
            </form>
        </div>
    )
}

export default RegisterPage