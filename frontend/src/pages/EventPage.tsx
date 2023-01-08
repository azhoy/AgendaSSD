import React, {useState, useEffect, useContext} from "react";
import AuthContext from "../context/AuthContext";
import {useNavigate, useSearchParams} from "react-router-dom";
import {decryptSymKey, generateEncryptedSymKey} from "../crypto/symmetricKeyFunctions";
import {CipherString, DecipherString} from "../crypto/cryptoclass";
import {decryptMessage, encryptMessage} from "../crypto/eventsFunctions";
import useAxios from "../utils/useAxios";
import {arrayBufferToBase64, base64ToArrayBuffer} from "../crypto/utils";
import {decryptPrivateKey, rsaDecrypt, rsaEncrypt} from "../crypto/AsymmetricKeyFunctions";

const EventPage = () => {
    const {authTokens, logoutUser, derivedKey} = useContext(AuthContext)
    const [eventInfo, setEventInfo] = useState([])
    const [isModifying, setIsModifying] = useState(false);
    const [isInviting, setIsInviting] = useState(false);
    const [searchParams] = useSearchParams();

    const navigate = useNavigate()
    const eventId = searchParams.get("eventId")
    let api = useAxios()

    interface UserPk {
        username: string;
        pk: number;
    }


    useEffect(()=> {
        getMyEventData()
    }, [])

    const findUser = (json: UserPk[], username: string): UserPk | undefined => {
        return json.find(user => user.username === username);
    }

    let getMyEventData = async () => {
        let eventData = await api.get(`/events/${eventId}/`)

        if (eventData.status === 200) {
            let data = await eventData.data
            let keys = sessionStorage.getItem("keys")
            if (keys) {
                let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
                const encryptedEventKey = data.protected_event_key
                let eventKey = await decryptSymKey(new DecipherString(encryptedEventKey), symKey)

                let title = new DecipherString(data.title)
                let end_date = new DecipherString(data.end_date)
                let start_date = new DecipherString(data.start_date)
                let description = new DecipherString(data.description)
                let location = new DecipherString(data.location)

                data.title = await (decryptMessage(title.ct, title.iv, eventKey))
                data.end_date = await(decryptMessage(end_date.ct, end_date.iv, eventKey))
                data.start_date = await(decryptMessage(start_date.ct, start_date.iv, eventKey))
                data.description = await(decryptMessage(description.ct, description.iv, eventKey))
                data.location = await(decryptMessage(location.ct, location.iv, eventKey))
                setEventInfo(data)
            }


        }else if (eventData.statusText === "Unauthorized"){
            logoutUser()
        }

    }

    const modifyEvent = async (eventId: string, field:string, newValue:string) => {
        let keys = sessionStorage.getItem("keys")
        if (keys) {
            let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
            const encryptedEventKey = eventInfo.protected_event_key
            let eventKey = await decryptSymKey(new DecipherString(encryptedEventKey), symKey)
            let encryptedValue = await encryptMessage(newValue, eventKey)
            let response = await api.put(`/events/${eventId}/`, { [field]: encryptedValue })
            if (response.status === 200) {
                await getMyEventData()
            }else{
                console.log("error")
            }
            }else{
            logoutUser()
        }

    }
    const inviteToEvent = async (eventId:string, username_to_invite:string, ) => {
        let keys = sessionStorage.getItem("keys")
        if (keys) {
            let symKey = await decryptSymKey(new DecipherString(JSON.parse(keys).protected_sym_key), derivedKey)
            const encryptedEventKey = eventInfo.protected_event_key
            let eventKey = await decryptSymKey(new DecipherString(encryptedEventKey), symKey)
            console.log(eventKey)
            const protectedEventId = await encryptMessage(eventId, eventKey)
            const protectedParticipantsUsers = await encryptMessage(eventInfo.participants+ " " + username_to_invite, eventKey)


            let response = await api.get(`/users/`)

            let pk= response.data.find( obj => obj.username === username_to_invite);
            if (pk){
                const publicKey = base64ToArrayBuffer(pk.public_key)
                const rsaEncryptedEventKey = new CipherString(0,new ArrayBuffer(16), await rsaEncrypt(eventKey,publicKey)).cipheredString
                let invitationRequest = await api.post(`/events/${eventId}/invitations/`, {username_to_invite:username_to_invite,
                    protected_event_key:rsaEncryptedEventKey, protected_event_id:protectedEventId, protected_participants_list: protectedParticipantsUsers
                })
                if (invitationRequest.status === 201){
                    console.log("success")
                }else{
                    console.log('error')
                }
            }else {
                alert("Not one of your contacts")
            }

    }}

    const inviteButtonClickHandler = async (event) => {
        try {
            event.preventDefault()
            await inviteToEvent(eventId, event.target.username_to_invite.value);
            setIsInviting(false)
        } catch (error) {
            console.error(error);
        }
    };


    return (
        <div>
            {isModifying ? (
                <div>
                    <p>Modify Event</p>
                    <input type="text" name="title" value={eventInfo.title} onChange={(event) => modifyEvent(eventId, event.target.name, event.target.value)} />
                    <input type="text" name="start_date" value={eventInfo.start_date} onChange={(event) => modifyEvent(eventId, event.target.name, event.target.value)} />
                    <input type="text" name="end_date" value={eventInfo.end_date} onChange={(event) => modifyEvent(eventId, event.target.name, event.target.value)} />
                    <input type="text" name="description" value={eventInfo.description} onChange={(event) => modifyEvent(eventId, event.target.name, event.target.value)} />
                    <input type="text" name="location" value={eventInfo.location} onChange={(event) => modifyEvent(eventId, event.target.name, event.target.value)} />
                    <button onClick={() => setIsModifying(false)}>End Modification</button>
                </div>
            ) : isInviting ? (
                <div>
                    <form onSubmit={inviteButtonClickHandler}>
                        <input type="text" name="username_to_invite"  />
                        <input type="submit"/>
                    </form>

                </div>):(
                <div>
                    <div>
                        <p>Creator : {eventInfo.creator_username}</p>
                        <p>Title : {eventInfo.title}</p>
                        <p>Start date : {eventInfo.start_date}</p>
                        <p>End date : {eventInfo.end_date}</p>
                        <p>Description : {eventInfo.description}</p>
                        <p>Location : {eventInfo.location}</p>
                        <p>Invited : {eventInfo.invited}</p>
                    </div>
                    <button onClick={() => setIsModifying(true)}>Modify Event</button>
                    <button onClick={() => setIsInviting(true)}>Add participants</button>

                </div>
            )}
        </div>
    );
}

export default EventPage