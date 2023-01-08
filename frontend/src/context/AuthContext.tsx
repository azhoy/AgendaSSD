import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import jwtDecode from "jwt-decode";
import { createMasterKey, createMasterKeyHash, deriveHKDF } from "../crypto/masterKeyFunctions";
import { arrayBufferToBase64 } from "../crypto/utils";

// Create the context
const AuthContext = createContext<{
    user: any | null;
    authTokens: { access: string; refresh: string } | null;
    derivedKey: ArrayBuffer;
    loginUser: (e: React.FormEvent<HTMLFormElement>) => Promise<void>;
    logoutUser: () => void;
    setUser: (user: any) => void;
    setAuthTokens: (authTokens: { access: string; refresh: string }) => void;
}>({
    user: null,
    authTokens: null,
    derivedKey: new ArrayBuffer(32),
    loginUser: async () => {},
    logoutUser: () => {},
    setUser: () => {},
    setAuthTokens: () => {},
});

// Export the context
export default AuthContext;

// Create the provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    // Initialize state variables
    const storedTokens = localStorage.getItem("authTokens")
    let [authTokens, setAuthTokens] = useState(() =>
        storedTokens
            ? JSON.parse(storedTokens)
            : null
    );
    let [user, setUser] = useState(() =>
        storedTokens ? jwtDecode(storedTokens) : null
    );
    let [loading, setLoading] = useState(true);
    let [derivedKey, setDerivedKey] = useState(new ArrayBuffer(32));

    // Get the navigate function from the router
    const navigate = useNavigate();

    // Define the login function
    let loginUser = async (e: React.FormEvent<HTMLFormElement>) => {
        // Prevent the default form submission behavior
        e.preventDefault();

        // Create the master key and hash it
        const masterKey = await createMasterKey(e.target.password.value, e.target.email.value);
        const masterKeyHash = arrayBufferToBase64(
            await createMasterKeyHash(masterKey, e.target.password.value)
        );

        // Send a request to the server to create a JWT
        let response = await fetch("http://127.0.0.1:8000/jwt/create/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: e.target.email.value, password: masterKeyHash }),
        });
        let data = await response.json();

        // If the request was successful, update state and local storage
        if (response.status == 200) {
            setAuthTokens(data);
            setUser(jwtDecode(data.access));
            setDerivedKey(await deriveHKDF(masterKey));
            localStorage.setItem("authTokens", JSON.stringify(data));
            await storeSessionKeys(data.access);
            navigate("/");
        } else {
            alert("Something went wrong !");
        }
    };

    // Define a function to store session keys
    let storeSessionKeys = async (auth: string) => {
        // Send a request to the server to get the session keys
        let response = await fetch("http://127.0.0.1:8000/users/me/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "JWT " + String(auth),
            },
        });
        let keys = await response.json();

        // If the request was successful, store the keys in session storage
        if (response.status == 200) {
            let { protected_symmetric_key, protected_private_key } = keys;
            console.log(protected_symmetric_key);
            sessionStorage.setItem("keys", JSON.stringify({ protected_sym_key: protected_symmetric_key, protected_private_key:protected_private_key }));
        } else {
            alert("Something went wrong !");
        }
    };

    // Define a function to log out the user
    let logoutUser = () => {
        // Clear the auth tokens and user data
        setAuthTokens(null);
        setUser(null);
        // Clear the data from local and session storage
        localStorage.removeItem("authTokens");
        sessionStorage.removeItem("keys");
        // Reset the derived key
        setDerivedKey(new ArrayBuffer(32));
        // Navigate to the login page
        navigate("/login");
    };

    // Create the context data object
    let contextData = {
        user,
        authTokens,
        derivedKey,
        loginUser,
        logoutUser,
        setUser,
        setAuthTokens,
    };

    // Use an effect to update the user data when the auth tokens change
    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access));
        }
        setLoading(false);
    }, [authTokens, loading]);

    // Render the provider component
    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
};