import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/Button";
import { StatusListbox } from "../components/StatusListbox";
import { Table } from "../components/Table";

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
            navigate("/:username/projects/")
    
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

    const shotColumns = [
        { key: "shot_name", header: "Shot Name" },
        { key: "status", header: "Status", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "status", newStatus)}
            />
        )},
        { key: "lay_status", header: "Layout", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "lay_status", newStatus)}
            />
        )},
        { key: "anim_status", header: "Animation", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "anim_status", newStatus)}
            />
        )},
        { key: "cfx_status", header: "CFX", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "cfx_status", newStatus)}
            />
        )},
        { key: "lit_status", header: "Lighting", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "lit_status", newStatus)}
            />
        )},
        { key: "assets_status", header: "Assets", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "assets_status", newStatus)}
            />
        )},
    ];
    console.log(shots && shots[0]);
    return (
        <div className="flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-screen ">
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">Project: {project.name}</h1>
                <br></br>
                {shots && shots.length > 0 ? (
                    <Table columns={shotColumns} rows={shots} />
                ) : (
                    <div>Not shots found for this project</div>
                )}
                <br></br>
                <div className="flex justify-center flex-row gap-1">
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded" title={"Delete project"} onClick={deleteProject}/>
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded" title={"Share project"} onClick={() => navigate(`/projects/${projectId}/share`)}/>
                </div>
             </div>
        </div>
    )
}