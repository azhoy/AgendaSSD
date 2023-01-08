import {CipherString, DecipherString} from "./cryptoclass";

let encoder = new TextEncoder()

export async function rsaGenerateKeyPair(): Promise<{privateKey:ArrayBuffer, publicKey:ArrayBuffer}> {
    const keyPair = await window.crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 4096,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256"
        },
        true,
        ["encrypt", "decrypt"]

    ) as CryptoKeyPair;
    const publicKey = await crypto.subtle.exportKey("spki", keyPair.publicKey);
    const privateKey = await crypto.subtle.exportKey("pkcs8", keyPair.privateKey);
    return {privateKey, publicKey};
}

export async function rsaEncrypt(data:ArrayBuffer, publicKey: ArrayBuffer): Promise<ArrayBuffer> {
    const rsaParams = {
        name: "RSA-OAEP",
        modulusLength: 4096,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: { name: "SHA-256"},
    };
    const impKey = await crypto.subtle.importKey('spki', publicKey, rsaParams, false, ["encrypt"])
    return await crypto.subtle.encrypt(rsaParams, impKey, data)
}

export async function rsaDecrypt(data: ArrayBuffer, privateKey: ArrayBuffer): Promise<ArrayBuffer> {
    const rsaParams = {
        name: "RSA-OAEP",
        modulusLength: 4096,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: { name: "SHA-256"},
    };
    const impKey = await crypto.subtle.importKey("pkcs8", privateKey, rsaParams, false, ["decrypt"]);
    return await crypto.subtle.decrypt(rsaParams, impKey, data);
}

export async function encryptPrivateKey(privateKey:ArrayBuffer, symKey:ArrayBuffer):Promise<string>{
    const ivArray = new Uint8Array(16)
    let iv = crypto.getRandomValues(ivArray)
    let encKey = await crypto.subtle.importKey("raw", symKey, "AES-GCM", false, ['encrypt'])
    let encryptedPrivateKey = await crypto.subtle.encrypt({name:"AES-GCM", iv:iv}, encKey, privateKey)
    return new CipherString(0, iv, encryptedPrivateKey).cipheredString
}

export async function decryptPrivateKey(privateKey:string, symKey:ArrayBuffer):Promise<ArrayBuffer>{
    let cipheredKey = new DecipherString(privateKey)
    let encKey = await crypto.subtle.importKey("raw", symKey, "AES-GCM", false, ['decrypt'])
    return await crypto.subtle.decrypt({name:"AES-GCM", iv:cipheredKey.iv}, encKey, cipheredKey.ct)


}