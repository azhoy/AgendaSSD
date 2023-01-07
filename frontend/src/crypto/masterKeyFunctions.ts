import {hkdfExpand} from "./cryptoUtils";

let encoder = new TextEncoder()
export async function generateMasterPassword(pwd:ArrayBuffer): Promise<CryptoKey> {
    return await window.crypto.subtle.importKey(
        "raw",
        pwd,
        "PBKDF2",
        false,
        ["deriveBits"],)
}
export async function createMasterKey(pwd:string, email:string): Promise<ArrayBuffer> {
    let pwdBuffer = encoder.encode(pwd)
    let emailBuffer = encoder.encode(email)

    return await window.crypto.subtle.deriveBits(
        {
            name: "PBKDF2",
            salt: emailBuffer,
            iterations: 100000,
            hash: "SHA-256",
        },
        await generateMasterPassword(pwdBuffer),
        256
    );
}

export async function createMasterKeyHash(masterKey:ArrayBuffer, pwd:string): Promise<ArrayBuffer> {
    let pwdBuffer = encoder.encode(pwd)
    return await window.crypto.subtle.deriveBits(
        {
            name: "PBKDF2",
            salt: pwdBuffer,
            iterations: 100000,
            hash: "SHA-256",
        },
        await generateMasterPassword(masterKey),
        256
    );
}

export async function  deriveHKDF(key: ArrayBuffer): Promise<ArrayBuffer> {
    const newKey = new Uint8Array(32);
    const encKey = await hkdfExpand(key, "enc", 32, "sha256");
    newKey.set(new Uint8Array(encKey));
    return  newKey;
}

export function bufferEqual (buf1:ArrayBuffer, buf2:ArrayBuffer) {
    if (buf1.byteLength != buf2.byteLength) return false;
    let dv1 = new Int8Array(buf1);
    let dv2 = new Int8Array(buf2);
    for (let i = 0 ; i != buf1.byteLength ; i++)
    {
        if (dv1[i] != dv2[i]) return false;
    }
    return true;
}