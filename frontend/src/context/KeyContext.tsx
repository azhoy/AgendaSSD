import React, { createContext, useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import {
    bufferEqual,
    createMasterKey,
    createMasterKeyHash,
    deriveHKDF,
} from "../crypto/masterKeyFunctions";
import { arrayBufferToBase64 } from "../crypto/utils";
import { decryptSymKey, generateEncryptedSymKey } from "../crypto/symmetricKeyFunctions";
import AuthContext from "./AuthContext";

import { DecipherString } from "../crypto/cryptoclass";
import { decryptMessage, encryptMessage } from "../crypto/eventsFunctions";
import useAxios from "../utils/useAxios";
import {encryptPrivateKey, rsaEncrypt, rsaGenerateKeyPair} from "../crypto/AsymmetricKeyFunctions";

// Create the KeyContext context
const KeyContext = createContext<{
    registerUser: (e: React.FormEvent<HTMLFormElement>) => Promise<void>;
}>({
    registerUser: async () => {},
});
export default KeyContext;

// Define the KeyProvider component
export const KeyProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const navigate = useNavigate();
    // Get the derived key and auth tokens from the AuthContext
    const { derivedKey, authTokens } = useContext(AuthContext);

    // Define a function to register a user
    let registerUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        // Get the master key from the entered password and email
        const masterKey = await createMasterKey(
            e.target.password.value,
            e.target.email.value
        );
        // Hash the master key
        const masterKeyHash = arrayBufferToBase64(
            await createMasterKeyHash(masterKey, e.target.password.value)
        );

        // Get the re-entered master key from the re-entered password and email
        const masterKeyVerify = await createMasterKey(
            e.target.re_password.value,
            e.target.email.value
        );
        // Hash the re-entered master key
        const masterKeyHashVerify = arrayBufferToBase64(
            await createMasterKeyHash(
                masterKeyVerify,
                e.target.re_password.value
            )
        );

        // If the master keys match
        if (bufferEqual(masterKey, masterKeyVerify)) {
            // Derive the master key
            const derivedMasterKey = await deriveHKDF(masterKey);
            // Generate an encrypted symmetric key
            const encryptedSymKey = await generateEncryptedSymKey(derivedMasterKey);
            // Generate an RSA key pair
            const rsaKeyPair = await rsaGenerateKeyPair();

            // Encrypt the private key with the symmetric key
            const protectedPrivateKey = await encryptPrivateKey(
                rsaKeyPair.privateKey,
                await decryptSymKey(new DecipherString(encryptedSymKey), derivedMasterKey)
            );
            // Convert the public key to a base64 string
            const publicKey = arrayBufferToBase64(rsaKeyPair.publicKey);

            // Send a request to the server to register the user
            try {
                const response = await fetch("http://127.0.0.1:8000/users/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: e.target.email.value,
                        username: e.target.username.value,
                        password: masterKeyHash,
                        re_password: masterKeyHashVerify,
                        public_key: publicKey,
                        protected_private_key: protectedPrivateKey,
                        protected_symmetric_key: encryptedSymKey,
                    }),
                });
                const data = await response.json();
                if (data.message === 'ok') {
                    alert('Registered ! Check your emails to activate your account');
                    navigate('login')
                } else {
                    console.log("Error Occured!");
                    console.log(data);
                }
            } catch (error) {
                console.error(error);
            }
        } else {
            console.log("Passwords don't match");
        }
    };

    // Define the context data
    let contextData = {
        registerUser: registerUser,
    };

    // Return the KeyContext.Provider component
    return (
        <KeyContext.Provider value={contextData}>
            {children}
        </KeyContext.Provider>
    );
};
