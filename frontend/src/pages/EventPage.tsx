import React, {useState, useEffect, useContext} from "react";
import AuthContext from "../context/AuthContext";
import {useSearchParams} from "react-router-dom";
import {decryptSymKey} from "../crypto/symmetricKeyFunctions";
import {DecipherString} from "../crypto/cryptoclass";
import {decryptMessage} from "../crypto/eventsFunctions";


const EventPage = () => {
    // @ts-ignore
    let {authTokens, logoutUser, derivedKey} = useContext(AuthContext)
    let [eventInfo, setEventInfo] = useState([])
    const [searchParams] = useSearchParams();
    const eventId = searchParams.get("eventId")


    useEffect(()=> {
        getMyEventData()
    }, [])

    let getMyEventData = async () => {
        let eventData = await fetch(`http://127.0.0.1:8000/events/${eventId}`, {
            method:'GET',
            headers:{
                'Authorization':'JWT ' + String(authTokens.access)
            }
        })

        if (eventData.status === 200) {
            let data = await eventData.json()
            let keys = sessionStorage.getItem("keys")
            if (keys) {
                let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
                let title = new DecipherString(data.title)
                let end_date = new DecipherString(data.end_date)
                let start_date = new DecipherString(data.start_date)
                let description = new DecipherString(data.description)
                let location = new DecipherString(data.location)

                data.title = await (decryptMessage(title.ct, title.iv, symKey))
                data.end_date = await(decryptMessage(end_date.ct, end_date.iv, symKey))
                data.start_date = await(decryptMessage(start_date.ct, start_date.iv, symKey))
                data.description = await(decryptMessage(description.ct, description.iv, symKey))
                data.location = await(decryptMessage(location.ct, location.iv, symKey))
                setEventInfo(data)
            }


        }else if (eventData.statusText === "Unauthorized"){
            logoutUser()
        }

    }

    return (
        <div>
            <p>Creator : {eventInfo.creator_username}</p>
            <p>Title : {eventInfo.title}</p>
            <p>Start date : {eventInfo.start_date}</p>
            <p>End date : {eventInfo.end_date}</p>
            <p>Description : {eventInfo.description}</p>
            <p>Location : {eventInfo.location}</p>
            <p>Invited : {eventInfo.invited}</p>
        </div>
    )
}

export default EventPage