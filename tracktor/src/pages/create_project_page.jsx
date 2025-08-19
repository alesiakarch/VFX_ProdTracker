import { use, useState } from "react"
import { NavigationType, useNavigate, useParams } from "react-router-dom"
import { Textbox } from "../components/Textbox"
import { Button } from "../components/Button"
import axios from "axios"

export function CreateProjectPage({projects, setProjects}) {

    const [projectName, setProjectName] = useState("")
    const [projectType, setProjectType] = useState("")
    const [shotsNum, setShotsNum] = useState([])
    const [projectDeadline, setProjectDeadline] = useState("")
    const { username } = useParams()
    const navigate = useNavigate()
    const user_id = localStorage.getItem("user_id")

    async function CreateProject() {
        if (!projectName.trim()) return;

        try {
            const response = await axios.post("http://localhost:8080/api/projects", {
                                            name:projectName,
                                            type:projectType,
                                            shotsNum: shotsNum,
                                            deadline: projectDeadline,
                                            user_id: user_id

                                        })

            setProjects([...projects, response.data])
            navigate(`/${username}/projects`)
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
        <div className="flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">
                Create New Project</h1>
                <label className="flex items-center justify-center">
                    Project name:
                    <Textbox className={"ml-2 bg-gray-200 rounded"}
                     value={projectName}
                     onChange={(e) => setProjectName(e.target.value)}/>
                </label>
                <br></br>
                <label className="flex items-center justify-center">
                    Project type:
                    <Textbox className={" ml-2 bg-gray-200 rounded"}
                     value={projectType}
                     onChange={(e) => setProjectType(e.target.value)}
                    />
                </label>
                <br></br>
                <label className="flex items-center justify-center">
                    Number of shots:
                    <Textbox className={" ml-2 bg-gray-200 rounded"}
                     value={shotsNum}
                     onChange={(e) => setShotsNum(Number(e.target.value))}
                    />
                </label>
                <br></br>
                <label className="flex items-center justify-center">
                    Project deadline:
                    <Textbox className={"ml-2 bg-gray-200 rounded"}
                     value={projectDeadline}
                     onChange={(e) => setProjectDeadline(e.target.value)}
                    />
                </label>
                 <Button className="mb-2 bg-amber-300 text-amber-700 px-4 py-2 rounded mt-2" title={"Create project!"} onClick={CreateProject}/>
                
            </div>

           
        </div>
    )
}