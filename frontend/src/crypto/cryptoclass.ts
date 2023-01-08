import { ICipherString, IDecipherString} from "./cryptoInterface";
import {arrayBufferToBase64, base64ToArrayBuffer} from "./utils";

export class CipherString implements ICipherString{
    encType: number;
    iv: ArrayBuffer;
    ct: ArrayBuffer;
    cipheredString: string;
    constructor(encType:number, iv:ArrayBuffer, ct:ArrayBuffer) {

        this.encType = encType;
        this.iv = iv;
        this.ct = ct;
        this.cipheredString = encType + '.' + arrayBufferToBase64(iv) + '|' + arrayBufferToBase64(ct);
    }
}

export class DecipherString implements IDecipherString{
    cipheredString: string;
    encType: number;
    iv: ArrayBuffer;
    ct: ArrayBuffer;
    constructor(cipheredString:string) {
        this.cipheredString = cipheredString
        let [first, ct] = cipheredString.split('|')
        let [enctype, iv ] = first.split(".")
        this.encType = +enctype;
        this.iv = base64ToArrayBuffer(iv);
        this.ct = base64ToArrayBuffer(ct);;
    }
}
