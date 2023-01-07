import {createContext, useState, useEffect, useContext} from "react";
import {useNavigate} from "react-router-dom";
import {bufferEqual, createMasterKey, createMasterKeyHash, deriveHKDF} from "../crypto/masterKeyFunctions";
import {arrayBufferToBase64} from "../crypto/utils";
import {decryptSymKey, generateEncryptedSymKey} from "../crypto/symmetricKeyFunctions";
import AuthContext from "./AuthContext";

import {DecipherString} from "../crypto/cryptoclass";
import {decryptMessage, encryptMessage} from "../crypto/eventsFunctions";
import useAxios from "../utils/useAxios";
import {encryptPrivateKey, rsaGenerateKeyPair} from "../crypto/AsymmetricKeyFunctions";
// @ts-ignore
const KeyContext = createContext()
export default KeyContext;

// @ts-ignore
export const KeyProvider = ({ children }) => {
    const navigate = useNavigate()
    const {derivedKey, authTokens} = useContext(AuthContext)

    // @ts-ignore
    let registerUser = async (e)=> {
        e.preventDefault()
        const masterKey = await createMasterKey(e.target.password.value, e.target.email.value)
        const masterKeyHash = arrayBufferToBase64(await createMasterKeyHash(masterKey, e.target.password.value))

        const masterKeyVerify = await createMasterKey(e.target.re_password.value, e.target.email.value)
        const masterKeyHashVerify = arrayBufferToBase64(await createMasterKeyHash(masterKeyVerify, e.target.re_password.value))

        if (bufferEqual(masterKey, masterKeyVerify)) {
            const derivedMasterKey = await deriveHKDF(masterKey)
            const encryptedSymKey =  await generateEncryptedSymKey(derivedMasterKey)
            const rsaKeyPair =  await rsaGenerateKeyPair()

            const protectedPrivateKey = await encryptPrivateKey(rsaKeyPair[0], await decryptSymKey(new DecipherString(encryptedSymKey), derivedMasterKey))
            const publicKey = arrayBufferToBase64(rsaKeyPair[1])

            let response = await fetch('http://127.0.0.1:8000/users/',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body: JSON.stringify({'email': e.target.email.value, "username":e.target.username.value, "password": masterKeyHash,
                    "re_password":masterKeyHashVerify, "public_key":publicKey, "protected_private_key":protectedPrivateKey,
                    'protected_symmetric_key':encryptedSymKey})
            })
            let data = await response.text()
            if (data === "") {
                console.log("Registered !")
            }else {
                console.log("Error Occured !")
                console.log(data)
            }

        }else{
            console.log('Passwords doesnt match')
        }
    }



    let contextData = {
        registerUser:registerUser,
    }

    return (
        // @ts-ignore
        <KeyContext.Provider value={contextData} >
            {children}
        </KeyContext.Provider>
    )
}
