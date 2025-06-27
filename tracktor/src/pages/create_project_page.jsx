import { useState } from "react"
import { NavigationType, useNavigate } from "react-router-dom"
import { Textbox } from "../components/Textbox"
import { Button } from "../components/Button"

export function CreateProjectPage({projects, setProjects}) {

    const [projectName, setProjectName] = useState("")
    const navigate = useNavigate()

    function CreateProject() {
        if (!projectName.trim()) return;

        const NewProject = {
            id: Date.now(),
            name: projectName
        }

        setProjects([...projects, NewProject])
        navigate("/")
    }
    return (
        <>
            <h1>Create New Project</h1>
            <Textbox className={"bg-gray-200"}/>
            <Button title={"Create project!"} onClick={CreateProject}/>
        </>
    )
}