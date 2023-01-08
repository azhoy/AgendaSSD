import React, { useEffect, useState } from "react";
import useAxios from "../utils/useAxios";
import { useNavigate } from "react-router-dom";

const ContactPage = () => {
    const [contacts, setContacts] = useState<{user_id: number, username: string}[]>([]);
    const [contactDemands, setContactDemands] = useState<{sender: string}[]>([]);
    const navigate = useNavigate();
    const api = useAxios();

    useEffect(() => {
        getMyContacts().then(() => {
            console.log("success")
        }).catch((error) => {
            console.log(error)
        });;
        showContactDemand().then(() => {
            console.log("success")
        }).catch((error) => {
            console.log(error)
        });
    }, []);

    const getMyContacts = async () => {
        const response = await api.get("/contacts/all/my_contacts/");
        if (response.status === 200) {
            const contacts = await response.data;
            console.log(response.data);
            setContacts(contacts);
        }
    };

    const showContactDemand = async () => {
        const response = await api.get("contacts/my_contact_requests/");
        if (response.status === 200) {
            const contactDemands = await response.data;
            setContactDemands(contactDemands);
        }
    };

    const acceptContactDemand = async (username: string) => {
        let response = await api.post("/contacts/accept_contact_requests/", {
            username_to_accept: username,
        });
        if (response.status === 201){
            alert('User added ! ')
            navigate('/')
        }else {
            alert('something bad happened !')
            navigate('/')
        }

    };

    const declineContactDemand = async (username: string) => {
        let response = await api.post("/contacts/decline_contact_requests/", {
            username_to_decline: username,
        });
        if (response.status === 201){
            alert('Invitation Declined ! ')
            navigate('/')
        }else {
            console.log(response.status)
            alert('something bad happened !')
            navigate('/')
        }
    };

    const deleteContact = async (username: string) => {
        let response = await api.post("/contacts/delete_contact/", { username_to_delete: username });
        if (response.status === 201){
            alert('Contact deleted ! ')
            navigate('/')
        }else {
            alert('something bad happened !')
            navigate('/')
        }
    };
    const addContact = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        let response = await api.post("/contacts/send_contact_request/", {
            username_to_add: e.currentTarget.username.value,
        });
        if (response.status === 201){
            alert('Invitation sent ! ')
            navigate('/')
        }else {
            alert('something bad happened !')
            navigate('/')
        }
    };

    return (
        <div>
            <p>Add New Contact </p>
            <form onSubmit={addContact}>
                <input
                    type="text"
                    name="username"
                    placeholder="Enter username to send an contact request"
                />
                <input type="submit" />
            </form>

            <p> Your Contacts</p>
            <ul>
                {contacts.map((contact) => (
                    <li key={contact.username}>
                        <p>{contact.username}</p>
                        <button onClick={() => deleteContact(contact.username)}>
                            Delete Contact
                        </button>
                    </li>
                ))}
            </ul>

            <p> Your Contact Demands </p>
            <ul>
                {contactDemands.map((contactDemand) => (
                    <li key={contactDemand.sender}>
                        <p>{contactDemand.sender}</p>
                        <button onClick={() => acceptContactDemand(contactDemand.sender)}>
                            Accept
                        </button>
                        <button onClick={() => declineContactDemand(contactDemand.sender)}>
                            Refuse
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ContactPage;

