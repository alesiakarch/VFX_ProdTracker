import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/Button";

export function ProjectPage({ reloadProjects }) {
    const { projectId } = useParams()
    const [project, setProject] = useState()
    const [shots, setShots] = useState()
    const navigate = useNavigate()

    useEffect(() => {
        const fetchProject = async () => {
            try {
                const project = await axios.get(`http://localhost:8080/api/projects/${projectId}`)
                setProject(project.data)

                const shots = await axios.get(`http://localhost:8080/api/projects/${projectId}/shots`)
                setShots(shots.data)
            } catch (error) {
                setProject(null)
                setShots(null)
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
            {shots && shots.length > 0 ? (
            <table>
                <thead>
                    <tr>
                        <th>Shot Name</th>
                        <th>Status</th>
                        <th>Layout</th>
                        <th>Animation</th>
                        <th>CFX</th>
                        <th>Lighting</th>
                        <th>Assets</th>
                    </tr>
                </thead>
                <tbody>
                    {shots.map((s) => (
                        <tr key={s.shot_id}>
                            <td>{s.shot_name}</td>
                            <td>{s.status}</td>
                            <td>{s.lay_status}</td>
                            <td>{s.anim_status}</td>
                            <td>{s.cfx_status}</td>
                            <td>{s.lit_status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            ) : (<div>Not shots found for this project</div>
            )}
            <Button title={"Delete project"} onClick={deleteProject}/>
        </>
    )
}