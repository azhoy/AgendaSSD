import React, {useContext, useEffect, useState} from "react";
import KeyContext from "../context/KeyContext";
import useAxios from "../utils/useAxios";
import {decryptSymKey} from "../crypto/symmetricKeyFunctions";
import {DecipherString} from "../crypto/cryptoclass";
import {decryptMessage, encryptMessage} from "../crypto/eventsFunctions";
import {Link, useNavigate} from "react-router-dom";
import AuthContext from "../context/AuthContext";
import registerPage from "./RegisterPage";

const ContactPage = () => {
    // @ts-ignore
    const [contacts, setContacts] = useState([])
    const [contactDemands, setContactDemands] = useState([])
    let navigate = useNavigate()
    let api = useAxios()

    useEffect(()=> {
        getMyContacts();
        showContactDemand()
    }, [])

    let getMyContacts = async () => {
        let response = await api.get('/contacts/all/my_contacts/')
        if (response.status === 200) {
            let contacts = await response.data
            console.log(response.data)
            setContacts(contacts)
        }
    }

    let showContactDemand = async () => {
        let response = await api.get('contacts/my_contact_requests')
        if (response.status === 200) {
            let contactDemands = await response.data
            setContactDemands(contactDemands)
        }
    }

    let acceptContactDemand = async (username:string) => {
        await api.post('/contacts/accept_contact_requests/', {username_to_accept:username})
    }

    let declineContactDemand = async (username:string) => {
        await api.post('/contacts/decline_contact_requests/', {username_to_decline:username})
    }

    let deleteContact = async (username:string) => {
        await api.post('/contacts/delete_contact/', {username_to_delete:username} )
    }
    let addContact = async (e) => {
        e.preventDefault()
        await api.post("/contacts/send_contact_request/", {username_to_add:e.target.username.value})
    }

    return (
        <div>
            <p>Add New Contact </p>
            <form onSubmit={(e) =>{addContact(e)}}>
                <input type="text" name="username" placeholder="Enter username to send an contact request"/>
                <input type="submit"/>
            </form>

            <p> Your Contacts</p>
            <ul>
                {contacts.map(contact => (
                    <li key={contact.user_id}>
                        <p>{contact.username}</p>
                        <button onClick={() => deleteContact(contact.username)}>Delete Contact</button>
                    </li>
                ))}
            </ul>

            <p> Your Contact Demands </p>
            <ul>
                {contactDemands.map(contactDemand => (
                    <li key={contactDemand.sender}>
                        <p>{contactDemand.sender}</p>
                        <button onClick={() => acceptContactDemand(contactDemand.sender)}>Accept</button>
                        <button onClick={() => declineContactDemand(contactDemand.sender)}>Refuse</button>

                    </li>
                ))}
            </ul>
        </div>
    )
}


export default ContactPage