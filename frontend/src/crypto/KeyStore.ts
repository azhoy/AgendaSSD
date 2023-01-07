const indexedDB = window.indexedDB

export function openDB(dataBaseName:string, dataBaseVersion:number) {
    const request = indexedDB.open(dataBaseName, dataBaseVersion);
    request.onerror = (err) => console.error(`IndexedDB error: ${request.error}`, err)
    request.onupgradeneeded = () => {
        const db = request.result;
        const store = db.createObjectStore("Keys", {keyPath:"id"});
        store.createIndex("symKey", ["symKey", "macKey"], {unique:true});
    }
    return request
}

export function storeKeys(symKey:CryptoKey, macKey:CryptoKey, dataBaseName:string, dataBaseVersion: number) {
    let request = openDB(dataBaseName, dataBaseVersion);
    request.onsuccess = () => {
        const db = request.result;
        const transaction = db.transaction("Keys", "readwrite");
        const store = transaction.objectStore("Keys");
        store.put({id:1, symKey:symKey, mackey:macKey });
        transaction.oncomplete = () => {db.close()}

    }
}

export async function getKeys(dataBaseName:string, dataBaseVersion: number) {
    return new Promise((resolve) => {
        const request = openDB(dataBaseName, dataBaseVersion);
        request.onsuccess = () => {
            const db = request.result;
            const transaction = db.transaction("Keys", "readwrite");
            const store = transaction.objectStore("Keys");
            const keys = store.get(1);
            keys.onsuccess = () => {
                resolve(keys.result);
            }
            keys.onerror = (err) => {
              console.error(`IndexedDB error: ${request.error}`, err);
            }
            transaction.oncomplete = () => {db.close()}
        }
    });
}
