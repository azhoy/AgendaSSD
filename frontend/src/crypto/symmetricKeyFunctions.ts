import {CipherString} from "./cryptoclass";

export  function generateSecretKey():object {
    const secretArray = new Uint8Array(32)
    const ivArray = new Uint8Array(16)
    let secret = crypto.getRandomValues(secretArray)
    let iv = crypto.getRandomValues(ivArray)
    return { secret: secret, iv: iv}
}

export async function generateEncryptedSymKey(derivedKey: ArrayBuffer) {
    let {secret, iv} = generateSecretKey()
    console.log(secret)
    let encKey = await crypto.subtle.importKey("raw", derivedKey, "AES-GCM", false, ['encrypt'] )
    let encryptedSymKey = await crypto.subtle.encrypt({name:"AES-GCM", iv:iv}, encKey, secret)
    return new CipherString(0, iv, encryptedSymKey).cipheredString
}

export async function decryptSymKey(encryptedSymKey: CipherString, derivedKey: ArrayBuffer) {
    let encKey = await crypto.subtle.importKey("raw", derivedKey, "AES-GCM", false, ['decrypt'] )
    return await crypto.subtle.decrypt({name: "AES-GCM", iv: encryptedSymKey.iv}, encKey, encryptedSymKey.ct)
}