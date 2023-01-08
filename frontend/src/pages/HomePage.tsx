import React, {useState, useEffect, useContext} from "react";
import AuthContext from "../context/AuthContext";
import {Link, useNavigate} from "react-router-dom";
import useAxios from "../utils/useAxios";
import {decryptMessage} from "../crypto/eventsFunctions";
import {CipherString, DecipherString} from "../crypto/cryptoclass";
import {decryptSymKey} from "../crypto/symmetricKeyFunctions";
import {decryptPrivateKey, rsaDecrypt} from "../crypto/AsymmetricKeyFunctions";
import {base64ToArrayBuffer} from "../crypto/utils";



const HomePage = () => {
    let [events, setEvents] = useState([])
    let [sharedEvents, setSharedEvents] = useState([])
    let {authTokens, logoutUser, derivedKey} = useContext(AuthContext)

    let api = useAxios()



    let navigate = useNavigate()
    useEffect(() => {
        getMyEvents().then(() => {
            console.log("success")
        }).catch((error) => {
            console.log(error)
        }), getSharedEvents()
    }, []);

    function handleEventClick(eventId:string) {
        navigate({pathname:"event", search:`?eventId=${eventId}`})
    }


    let getMyEvents = async () => {
        let response = await api.get('/events/my_events/')
        if (response.status === 200) {
            const decryptedEvents = response.data.map(async event => {
                let keys = sessionStorage.getItem("keys")
                if (keys) {
                    let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
                    const encryptedEventKey = event.protected_event_key
                    console.log(event.protected_event_key)
                    let eventKey = await decryptSymKey(new DecipherString(encryptedEventKey), symKey)
                    let title = new DecipherString(event.title)
                    event.title = await (decryptMessage(title.ct, title.iv, eventKey))
                    return event;
                } else {console.log('No Keys')}
        })
            setEvents(await Promise.all(decryptedEvents))
    }}

    let getSharedEvents = async () => {
        let preSharedEvents = []
        let keys = sessionStorage.getItem("keys")
        if (keys) {
            const {protected_private_key, protected_sym_key} = sessionStorage.getItem("keys")? JSON.parse(sessionStorage.getItem("keys")):null
            let symKey = await decryptSymKey(new DecipherString(protected_sym_key), derivedKey)
            const decrypted_private_key = await decryptPrivateKey(protected_private_key, symKey)
            let response = await api.get('/events/my_invitations/')
            if (response.status === 200) {

                for (let i =0; i<response.data.length; i++) {
                    try{
                        let data = new DecipherString(response.data[i].protected_event_key).ct
                        await rsaDecrypt(data, decrypted_private_key)
                        preSharedEvents.push(response.data[i])
                    }
                    catch (error){
                        console.log(error)
                    }

                }
                let decipheredSharedEvents = []
                preSharedEvents.map(async preSharedEvent =>{
                    let cipheredEventId = new DecipherString(preSharedEvent.protected_event_id)
                    let cipheredEventKey = new DecipherString(preSharedEvent.protected_event_key)
                    let eventKey = await rsaDecrypt(cipheredEventKey.ct, decrypted_private_key)
                    let sharedEventId = await decryptMessage(cipheredEventId.ct, cipheredEventId.iv, eventKey)
                    const sharedEventsTotal = await api.get(`/contacts_events/${sharedEventId}/`)
                    if (sharedEventsTotal.status){
                        let data = sharedEventsTotal.data

                        let title = new DecipherString(data.title)
                        let end_date = new DecipherString(data.end_date)
                        let start_date = new DecipherString(data.start_date)
                        let description = new DecipherString(data.description)
                        let location = new DecipherString(data.location)
                        let participants = new DecipherString(data.participants)

                        data.title = await (decryptMessage(title.ct, title.iv, eventKey))
                        data.end_date = await(decryptMessage(end_date.ct, end_date.iv, eventKey))
                        data.start_date = await(decryptMessage(start_date.ct, start_date.iv, eventKey))
                        data.description = await(decryptMessage(description.ct, description.iv, eventKey))
                        data.location = await(decryptMessage(location.ct, location.iv, eventKey))
                        data.participants = await(decryptMessage(participants.ct, participants.iv, eventKey))

                        decipheredSharedEvents.push(data)

                    }
                    setSharedEvents(decipheredSharedEvents)

                })
            }
        }
    }

    const deleteEvent = async (eventId: string) => {
        let response = await api.delete(`/events/${eventId}/`)
        if (response.status === 204){
            // Get the updated list of events
             await getMyEvents();

        }else{
            console.log('error', response.statusText)
        }
    };



    return (
        <div>
            <Link to='/createEvent'>Create Event</Link>
            <p> You are logged to the home page !</p>
            <ul>
                {events.map(event => (
                    <div>
                        <li key={event.event_id} onClick={()=>{handleEventClick(event.event_id)}}>{event.title}</li>
                        <button onClick={() => deleteEvent(event.event_id)}>
                            Delete Event
                        </button>
                    </div>
                ))}
            </ul>
            {sharedEvents ? (
                    <ul>
                        <h3>Events Shared with me </h3>
                        {sharedEvents.map(sharedEvent => (
                            <div>
                                <li key={sharedEvent.event_id}>
                                    <p>Title: {sharedEvent.title}</p>
                                    <p>Start Date:  {sharedEvent.start_date}</p>
                                    <p>End date:  {sharedEvent.end_date}</p>
                                    <p>Description: {sharedEvent.description}</p>
                                    <p>Location: {sharedEvent.location}</p>
                                    <p>Participants: {sharedEvent.participants}</p>
                                    <p>Creator Username:  {sharedEvent.creator_username}</p>
                                </li>
                            </div>
                        ))}
                    </ul>
                ):(
                    <ul>
                        <li>No shared Event yet</li>
                    </ul>
            )

            }


        </div>
    )
}

export default HomePage