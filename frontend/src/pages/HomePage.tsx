import React, {useState, useEffect, useContext} from "react";
import AuthContext from "../context/AuthContext";
import {Link, useNavigate} from "react-router-dom";
import useAxios from "../utils/useAxios";
import {decryptMessage} from "../crypto/eventsFunctions";
import {DecipherString} from "../crypto/cryptoclass";
import {decryptSymKey} from "../crypto/symmetricKeyFunctions";



const HomePage = () => {
    let [events, setEvents] = useState([])
    // @ts-ignore
    let {authTokens, logoutUser, derivedKey} = useContext(AuthContext)

    let api = useAxios()

    let navigate = useNavigate()
    useEffect(()=> {
        getMyEvents()
    }, [])

    function handleEventClick(eventId:string) {
        navigate({pathname:"event", search:`?eventId=${eventId}`})
    }


    let getMyEvents = async () => {
        let response = await api.get('/events/my_events')
        if (response.status === 200) {
            const decryptedEvents = response.data.map(async event => {
                let keys = sessionStorage.getItem("keys")
                if (keys) {
                    let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
                    let title = new DecipherString(event.title)
                    event.title = await (decryptMessage(title.ct, title.iv, symKey))
                    return event;
                }
        })
            setEvents(await Promise.all(decryptedEvents))
    }}

    return (
        <div>
            <Link to='/createEvent'>Create Event</Link>
            <p> You are logged to the home page !</p>
            <ul>
                {events.map(event => (
                    <li key={event.event_id} onClick={()=>{handleEventClick(event.event_id)}}>{event.title}</li>
                ))}
            </ul>
        </div>
    )
}

export default HomePage