import React, {useContext} from "react";
import AuthContext from "../context/AuthContext";

const LoginPage = () => {
    // @ts-ignore
    let {loginUser} = useContext(AuthContext)
    return (
        <div>
            <form onSubmit={loginUser}>
                <input type="text" name="email" placeholder="Enter Email"/>
                <input type="password" name="password" placeholder="Enter your password" />
                <input type="submit" />
            </form>
        </div>
    )
}

export default LoginPage