import {createContext, useState, useEffect, useContext} from "react";
import {useNavigate} from "react-router-dom";
import jwtDecode from "jwt-decode";
import {createMasterKey, createMasterKeyHash, deriveHKDF} from "../crypto/masterKeyFunctions";
import {arrayBufferToBase64} from "../crypto/utils";

// @ts-ignore
const AuthContext = createContext()
export default AuthContext;


// @ts-ignore
export const AuthProvider = ({ children }) => {
    // @ts-ignore
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null)
    // @ts-ignore
    let [user, setUser] = useState(() => localStorage.getItem("authTokens") ? jwtDecode(localStorage.getItem("authTokens")) : null)
    let [loading, setLoading] = useState(true)
    let [derivedKey, setDerivedKey] = useState(new ArrayBuffer(32))


    const navigate = useNavigate()
    // @ts-ignore
    let loginUser = async (e)=> {
        e.preventDefault()
        const masterKey = await createMasterKey(e.target.password.value, e.target.email.value)
        const masterKeyHash = arrayBufferToBase64(await createMasterKeyHash(masterKey, e.target.password.value))

        let response = await fetch('http://127.0.0.1:8000/jwt/create/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
            },
            body: JSON.stringify({'email': e.target.email.value, "password": masterKeyHash})
        })
        let data = await response.json()

        if (response.status == 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            setDerivedKey(await deriveHKDF(masterKey))
            localStorage.setItem('authTokens',JSON.stringify(data))
            await storeSessionKeys(data.access)
            navigate('/')
        }else{
            alert('Something went wrong !')
        }

    }
    let storeSessionKeys = async (auth) => {
        let response = await fetch('http://127.0.0.1:8000/users/me',{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'JWT ' + String(auth)
            }
        })
        let keys = await response.json()
        if (response.status == 200) {
            let {protected_symmetric_key} = keys
            console.log(protected_symmetric_key)
            sessionStorage.setItem('keys',JSON.stringify({protected_sym_key:protected_symmetric_key}))
        }else{
            alert('Something went wrong !')
        }

    }
    let logoutUser = () =>{
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
        sessionStorage.removeItem('keys')
        setDerivedKey(new ArrayBuffer(32))
        navigate('/login')
    }


    let contextData = {
        user:user,
        authTokens:authTokens,
        derivedKey:derivedKey,
        loginUser:loginUser,
        logoutUser:logoutUser,
        setUser:setUser,
        setAuthTokens:setAuthTokens,
    }

    useEffect(()=> {

        if(authTokens){
            setUser(jwtDecode(authTokens.access))
        }
        setLoading(false)

    }, [authTokens, loading])

    return(
        <AuthContext.Provider value={contextData} >
            {loading ? null : children}
        </AuthContext.Provider>
    )

}
