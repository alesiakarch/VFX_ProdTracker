import axios from "axios"
import { Button } from "../components/Button"   
import { Textbox } from "../components/Textbox"
import { useParams } from "react-router-dom"
import { useState } from "react"


export function JoinProjectPage() {
    const [sharecode, setSharecode] = useState("")
    const [message, setMessage] = useState("")

    async function JoinProject() {
        const user_id = localStorage.getItem("user_id")
        if (!sharecode || !user_id) {
            setMessage("Missing project code or user ID")
            return
        }
        try {
            const response = await axios.post(`http://localhost:8080/api/join_project`,{
                                                sharecode,
                                                user_id
                                            })
            setMessage("Project added successfully")
        } catch (error) {
            setMessage(error.response?.data?.error || "Failed to join project")
        }
    }

    return (
        <div className="flex flex-col space-y-4">
            <h1>Enter the project code to add it to your projects</h1>
            <label>
                Project code:
                    <Textbox className={"bg-gray-200"}
                    value={sharecode}
                    onChange={(e) => setSharecode(e.target.value)}/>
            </label>
            <Button title={"Add project"} onClick={JoinProject}/>
            {message && <div>{message}</div>}
        </div>
    )
}