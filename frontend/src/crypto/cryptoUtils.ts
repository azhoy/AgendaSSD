let encoder = new TextEncoder()

export async function  hmac(
    value: ArrayBuffer,
    key: ArrayBuffer,
    algorithm: "sha1" | "sha256" | "sha512"
): Promise<ArrayBuffer> {
    const signingAlgorithm = {
        name: "HMAC",
        hash: { name: algorithm === "sha1" ? "SHA-1" : algorithm === "sha256" ? "SHA-256" : "SHA-512" },
    };

    const impKey = await crypto.subtle.importKey("raw", key, signingAlgorithm, false, ["sign"]);
    return await crypto.subtle.sign(signingAlgorithm, impKey, value);
}

export async function hkdfExpand(
    prk: ArrayBuffer,
    info: string,
    outputByteSize: number,
    algorithm: "sha256" | "sha512"
): Promise<ArrayBuffer> {
    const hashLen = algorithm === "sha256" ? 32 : 64;
    if (outputByteSize > 255 * hashLen) {
    throw new Error("outputByteSize is too large.");
}
const prkArr = new Uint8Array(prk);
if (prkArr.length < hashLen) {
    throw new Error("prk is too small.");
}
const infoBuf = encoder.encode(info);
const infoArr = new Uint8Array(infoBuf);
let runningOkmLength = 0;
let previousT = new Uint8Array(0);
const n = Math.ceil(outputByteSize / hashLen);
const okm = new Uint8Array(n * hashLen);
for (let i = 0; i < n; i++) {
    const t = new Uint8Array(previousT.length + infoArr.length + 1);
    t.set(previousT);
    t.set(infoArr, previousT.length);
    t.set([i + 1], t.length - 1);
    previousT = new Uint8Array(await hmac(t.buffer, prk, algorithm));
    okm.set(previousT, runningOkmLength);
    runningOkmLength += previousT.length;
    if (runningOkmLength >= outputByteSize) {
        break;
    }
}
return okm.slice(0, outputByteSize).buffer;
}

export async function macsEqual(mac1Data:ArrayBuffer, mac2Data:ArrayBuffer, key:ArrayBuffer) {
    const alg = {
        name: 'HMAC',
        hash: { name: 'SHA-256' }
    };

    const importedMacKey = await window.crypto.subtle.importKey('raw', key, alg, false, ['sign']);
    const mac1 = await window.crypto.subtle.sign(alg, importedMacKey, mac1Data);
    const mac2 = await window.crypto.subtle.sign(alg, importedMacKey, mac2Data);

    if (mac1.byteLength !== mac2.byteLength) {
        return false;
    }

    const arr1 = new Uint8Array(mac1);
    const arr2 = new Uint8Array(mac2);

    for (let i = 0; i < arr2.length; i++) {
        if (arr1[i] !== arr2[i]) {
            return false;
        }
    }

    return true;
}


