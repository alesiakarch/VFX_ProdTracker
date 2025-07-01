import { use, useState } from "react"
import { NavigationType, useNavigate } from "react-router-dom"
import { Textbox } from "../components/Textbox"
import { Button } from "../components/Button"
import axios from "axios"

export function CreateProjectPage({projects, setProjects}) {

    const [projectName, setProjectName] = useState("")
    const [projectType, setProjectType] = useState("")
    const [shotsNum, setShotsNum] = useState([])
    const [projectDeadline, setProjectDeadline] = useState("")
    const navigate = useNavigate()

    async function CreateProject() {
        if (!projectName.trim()) return;

        try {
            const response = await axios.post("http://localhost:8080/api/projects", {
                                            name:projectName,
                                            type:projectType,
                                            shotsNum: shotsNum,
                                            deadline: projectDeadline    
                                        })

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
            <br></br>
            <div>
                <label>
                    Project name:
                    <Textbox className={"bg-gray-200"}
                     value={projectName}
                     onChange={(e) => setProjectName(e.target.value)}/>
                </label>
                <br></br>
                <label>
                    Project type:
                    <Textbox className={"bg-gray-200"}
                     value={projectType}
                     onChange={(e) => setProjectType(e.target.value)}
                    />
                </label>
                <br></br>
                <label>
                    Number of shots:
                    <Textbox className={"bg-gray-200"}
                     value={shotsNum}
                     onChange={(e) => setShotsNum(Number(e.target.value))}
                    />
                </label>
                <br></br>
                <label>
                    Project deadline:
                    <Textbox className={"bg-gray-200"}
                     value={projectDeadline}
                     onChange={(e) => setProjectDeadline(e.target.value)}
                    />
                </label>
                
            </div>
            <br></br>
            <Button title={"Create project!"} onClick={CreateProject}/>
        </>
    )
}