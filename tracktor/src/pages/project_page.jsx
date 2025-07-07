import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/Button";
import { StatusListbox } from "../components/StatusListbox";

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

    const updateShotField = async(shot_id, field, newStatus) => {
        try {
            await axios.patch(`http://localhost:8080/api/projects/${projectId}/shots/${shot_id}`,
                 {status_item : field, value : newStatus})
            setShots(shots =>
                shots.map(shot =>
                    shot.shot_id === shot_id ? {...shot, [field] : newStatus} : shot
                )
            )
        } catch (error) {
            alert("Failed to update status")
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
                            <td>
                                <StatusListbox value={s.status} 
                                onChange={newStatus => updateShotField(s.shot_id, "status", newStatus)}
                                />
                            </td>
                            <td>
                                <StatusListbox value={s.lay_status} 
                                onChange={newStatus => updateShotField(s.shot_id, "lay_status", newStatus)}
                                /></td>
                            <td>
                                <StatusListbox value={s.anim_status} 
                                onChange={newStatus => updateShotField(s.shot_id, "anim_status", newStatus)}
                                />
                            </td>
                            <td>
                                <StatusListbox value={s.cfx_status} 
                                onChange={newStatus => updateShotField(s.shot_id, "cfx_status", newStatus)}
                                />    
                            </td>
                            <td>
                                <StatusListbox value={s.status} 
                                onChange={newStatus => updateShotField(s.shot_id, "status", newStatus)}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            ) : (<div>Not shots found for this project</div>
            )}
            <br></br>
            <Button title={"Delete project"} onClick={deleteProject}/>
        </>
    )
}