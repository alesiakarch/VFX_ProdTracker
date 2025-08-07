import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import { Button } from "../components/Button"
import { Popup } from "../components/Popup"
import axios from "axios"


export function NotesPage(){
    const { projectId, itemId, itemType, itemDept} = useParams()
    const [notes, setNotes] = useState([])
    const [popupOpen, setPopupOpen] = useState(false)
    const [popupFields, setPopupFields] = useState([])

    useEffect(() => {
        const fetchItem = async () => {
            try {
                const notes = await axios.get(`http://localhost:8080/api/projects/${projectId}/${itemType}/${itemId}/${itemDept}/notes`)
                setNotes(notes.data)
            } catch (error) {
                setNotes(null)
            }
        }
        fetchItem()
    }, [itemId, itemType, itemDept])

    const handleAddNoteClick = () => {
        setPopupFields([{name: "note_body", label: "Note: ", required: true}])
        setPopupOpen(true)
    }

    async function CreateNote(formData) {
        if (!formData.note_body.trim()) return
        
        try {
            const response = await axios.post(`http://localhost:8080/api/projects/${projectId}/${itemType}/${itemId}/${itemDept}/notes`, {
                note_body: formData.note_body
            })
            setNotes([...notes, response.data])
            setPopupOpen(false)
        } catch (error) {
            console.error("Axios error object:", error);
            if (error.response) {
                console.error("Axios error response:", error.response);
            }
            if (error.request) {
                console.error("Axios error request:", error.request);
            }
            if (error.message) {
                console.error("Axios error message:", error.message);
            }
            alert("Failed to create note")
        }
    }


    console.log("itemType:", itemType, "department:", itemDept);

    return (
        <div className="flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-screen">
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">Notes: </h1>
                <Button
                    className={"text_left px-4 py-2 rounded-t bg-amber-300 text-white font-bold"}
                    onClick={handleAddNoteClick}
                    title={`Add ${itemDept.toUpperCase()} note`}
                />

            </div>
            <Popup
                open={popupOpen}
                onClose={() => setPopupOpen(false)}
                onSubmit={CreateNote}
                fields={popupFields}
            />

        </div>
    )
}