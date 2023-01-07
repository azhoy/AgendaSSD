import React from 'react';
import { Navigate } from 'react-router-dom';
import {useContext} from "react";
import AuthContext from "../context/AuthContext";
import KeyContext from "../context/KeyContext";

// @ts-ignore
function RequireAuth({ children, redirectTo }) {
    let {user} = useContext(AuthContext)
    return user ? children : <Navigate to={redirectTo} />;
}
export default RequireAuth;