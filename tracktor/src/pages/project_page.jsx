import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/Button";

export function ProjectPage({ reloadProjects }) {
    const { projectId } = useParams()
    const [project, setProject] = useState()
    const navigate = useNavigate()

    useEffect(() => {
        const fetchProject = async () => {
            try {
                const project = await axios.get(`http://localhost:8080/api/projects/${projectId}`)
                setProject(project.data)
            } catch (error) {
                setProject(null)
            }
        }
        fetchProject()
    },[projectId])

    const deleteProject = async () => {
        try {
            await axios.delete(`http://localhost:8080/api/projects/${projectId}`)
            alert("Project deleted!")
            navigate("/")
    
        } catch (error) {
            alert("Failed to delete project")
        }
    }

    if (project === undefined) return <div>Loading...</div>
    if (project === null) return <div>Project not found</div>
    return (
        <>
            <h1>Project: {project.name}</h1>
            <br></br>
            
            <Button title={"Delete project"} onClick={deleteProject}/>
        </>
    )
}