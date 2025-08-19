import axios from "axios"
import { useState } from "react"
import { Button } from "../components/Button"
import { Textbox } from "../components/Textbox"


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
        <div className="flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded p-8 w-full max-w-full">
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">Enter the project code to add it to your projects</h1>
                <label>
                    Project code:
                        <Textbox className={"ml-2 bg-gray-200 rounded"}
                        value={sharecode}
                        onChange={(e) => setSharecode(e.target.value)}/>
                </label>
                <Button className="bg-amber-300 text-amber-700 px-4 py-2 rounded mt-2" title={"Add project"} onClick={JoinProject}/>
                {message && <div>{message}</div>}
            </div>                
        </div>
    )
}