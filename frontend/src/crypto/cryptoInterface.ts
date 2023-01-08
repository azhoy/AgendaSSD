export interface ICipherString {
    encType: number;
    iv: ArrayBuffer;
    ct: ArrayBuffer;
    cipheredString: string;
}

export interface IDecipherString {
    cipheredString: string;
}