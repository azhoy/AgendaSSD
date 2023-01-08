import React, {useContext} from "react";
import useAxios from "../utils/useAxios";
import {decryptSymKey, generateEncryptedSymKey, generateSecretKey} from "../crypto/symmetricKeyFunctions";
import {DecipherString} from "../crypto/cryptoclass";
import {encryptMessage} from "../crypto/eventsFunctions";
import {useNavigate} from "react-router-dom";
import AuthContext from "../context/AuthContext";

const CreateEventPage = () => {
    let {derivedKey, logoutUser} = useContext(AuthContext)
    let navigate = useNavigate()
    let api = useAxios()

    let handleSubmit = (e:React.FormEvent<HTMLFormElement>) => {
        createEvent(e).then(r => {
            navigate('/')}).catch(error => {
                console.error(error)
            logoutUser()
        })
        }

    let createEvent = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        let keys = sessionStorage.getItem("keys")
        if (keys) {
            let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
            const encryptedEventKey = await generateEncryptedSymKey(symKey)
            let eventKey = await decryptSymKey(new DecipherString(encryptedEventKey), symKey)
            symKey = new ArrayBuffer(32)
            const encryptedTitle = await encryptMessage(e.target.title.value, eventKey)
            console.log(encryptedTitle)
            const encryptedStartDate = await encryptMessage(e.target.start_date.value, eventKey)
            const encryptedEndDate = await encryptMessage(e.target.end_date.value, eventKey)
            const encryptedDescription = await encryptMessage(e.target.description.value, eventKey)
            const encryptedLocation = await encryptMessage(e.target.location.value, eventKey)
            eventKey = new ArrayBuffer(32)
            const response = await api.post('create_events/',{'protected_event_key': encryptedEventKey, "title":encryptedTitle, "start_date": encryptedStartDate,
                "end_date":encryptedEndDate, "description":encryptedDescription, "location":encryptedLocation})
            const data = await response
            console.log(data)
        }else{
            logoutUser()
        }
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="text" name="title" placeholder="Enter title"/>
                <input type="text" name="start_date" placeholder="Enter start_date"/>
                <input type="text" name="end_date" placeholder="Enter end_date"/>
                <input type="text" name="description" placeholder="Enter description"/>
                <input type="text" name="location" placeholder="Enter location"/>
                <input type="submit" />
            </form>
        </div>
    )
}

export default CreateEventPage;
