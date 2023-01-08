import React from 'react';
import { Navigate } from 'react-router-dom';
import {useContext} from "react";
import AuthContext from "../context/AuthContext";

function RequireAuth({ children, redirectTo }: { children: React.ReactNode, redirectTo: string }) {
    let {user} = useContext(AuthContext)
    return user ? children : <Navigate to={redirectTo} />;
}
export default RequireAuth;