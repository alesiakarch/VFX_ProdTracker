import { useState } from "react"
import { NavigationType, useNavigate } from "react-router-dom"
import { Textbox } from "../components/Textbox"
import { Button } from "../components/Button"
import axios from "axios"

export function CreateProjectPage({projects, setProjects}) {

    const [projectName, setProjectName] = useState("")
    const navigate = useNavigate()

    async function CreateProject() {
        if (!projectName.trim()) return;

        try {
            const response = await axios.post("http://localhost:8080/api/projects", {name:projectName})

            setProjects([...projects, response.data])
            navigate("/")
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
            alert("Failed to create project")
        }
    }
    return (
        <>
            <h1>Create New Project</h1>
            <Textbox className={"bg-gray-200"}
                     value={projectName}
                     onChange={(e) => setProjectName(e.target.value)}/>
            <Button title={"Create project!"} onClick={CreateProject}/>
        </>
    )
}