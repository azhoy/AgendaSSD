import React, {useContext, useEffect} from "react";
import KeyContext from "../context/KeyContext";
import useAxios from "../utils/useAxios";
import {decryptSymKey} from "../crypto/symmetricKeyFunctions";
import {DecipherString} from "../crypto/cryptoclass";
import {encryptMessage} from "../crypto/eventsFunctions";
import {useNavigate} from "react-router-dom";
import AuthContext from "../context/AuthContext";

const CreateEventPage = () => {
    // @ts-ignore
    let {derivedKey} = useContext(AuthContext)
    let navigate = useNavigate()
    let api = useAxios()

    useEffect(()=> {
        createEvent()
    }, [])

    let createEvent = async (e) => {
        e.preventDefault()

        let keys = sessionStorage.getItem("keys")
        if (keys) {
            let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
            let encryptedEventKey = await encryptMessage(e.target.protected_event_key.value, symKey)
            let encryptedTitle = await encryptMessage(e.target.title.value, symKey)
            let encryptedStartDate = await encryptMessage(e.target.start_date.value, symKey)
            let encryptedEndDate = await encryptMessage(e.target.end_date.value, symKey)
            let encryptedDescription = await encryptMessage(e.target.description.value, symKey)
            let encryptedLocation = await encryptMessage(e.target.location.value, symKey)
            let response = await api.post('create_events/',{'protected_event_key': encryptedEventKey, "title":encryptedTitle, "start_date": encryptedStartDate,
                "end_date":encryptedEndDate, "description":encryptedDescription, "location":encryptedLocation})

            let data = await response
            console.log(data)
        }}
    return (
        <div>
            <form onSubmit={createEvent}>
                <input type="text" name="protected_event_key" placeholder="Enter protected_event_key"/>
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

export default CreateEventPage