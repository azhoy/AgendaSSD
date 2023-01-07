import {getKeys} from "./KeyStore";
import {CipherString} from "./cryptoclass";
import {arrayBufferToBase64} from "./utils";

let decoder = new TextDecoder()
let encoder = new TextEncoder()

export async function encryptMessage(message:string, symKey: ArrayBuffer) {
    const ivArray = new Uint8Array(16)
    let iv = crypto.getRandomValues(ivArray)
    let encKey = await crypto.subtle.importKey("raw", symKey, "AES-GCM", false, ['encrypt'] )
    let encryptedMessage = await crypto.subtle.encrypt({name:"AES-GCM", iv:iv}, encKey, encoder.encode(message))
    return new CipherString(0, iv, encryptedMessage).cipheredString
}

export async function decryptMessage(encryptedMessage: ArrayBuffer, iv: ArrayBuffer, symKey:ArrayBuffer) {
    let decKey = await crypto.subtle.importKey("raw", symKey, "AES-GCM", false, ['decrypt'] )
    return decoder.decode(await crypto.subtle.decrypt({name: "AES-GCM", iv: iv}, decKey, encryptedMessage))
}
