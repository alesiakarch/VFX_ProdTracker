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
    const [assets, setAssets] = useState()
    const [activeTab, setActiveTab] = useState("shots")
    const navigate = useNavigate()

    useEffect(() => {
        const fetchProject = async () => {
            try {
                const project = await axios.get(`http://localhost:8080/api/projects/${projectId}`)
                setProject(project.data)

                const shots = await axios.get(`http://localhost:8080/api/projects/${projectId}/shots`)
                setShots(shots.data)

                const assets = await axios.get(`http://localhost:8080/api/projects/${projectId}/assets`)
                setAssets(assets.data)

            } catch (error) {
                setProject(null)
                setShots(null)
                setAssets(null)
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
            alert("Failed to update shot status")
        }
    }

    const updateAssetField = async(asset_id, field, newStatus) => {
        try {
            await axios.patch(`http://localhost:8080/api/projects/${projectId}/shots/${shot_id}`,
                 {status_item : field, value : newStatus})
            setAssets(assets =>
                assets.map(asset =>
                    asset.asset_id === asset_id ? {...asset, [field] : newStatus} : asset
                )
            )
        } catch (error) {
            alert("Failed to update asset status")
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

    const assetColumns = [
        { key: "asset_name", header: "Asset Name" },
        { key: "status", header: "Status", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "status", newStatus)}
            />
        )},
        { key: "mod_status", header: "Modelling", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.shot_id, "lay_status", newStatus)}
            />
        )},
        { key: "srf_status", header: "Surfacing", render: (value, row) => (
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
    ];

    return (
        <div className="flex items-center justify-center min-h-screen bg-amber-50">


            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-screen ">
                <div className="flex gap-2 mb-6">
                    <Button className={`px-4 py-2 rounded-t ${activeTab === "shots" ? "bg-amber-300 text-white font-bold" : "bg-gray-100 text-amber-800"}`}
                    onClick={() => setActiveTab("shots")}
                    title={"Shots"}/>
                    <Button className={`px-4 py-2 rounded-t ${activeTab === "assets" ? "bg-amber-300 text-white font-bold" : "bg-gray-100 text-amber-800"}`}
                    onClick={() => setActiveTab("assets")}
                    title={"Assets"}/>
                </div>
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">Project: {project.name}</h1>
                {activeTab === "shots" && (
                    <>
                    {shots && shots.length > 0 ? (
                    <Table columns={shotColumns} rows={shots} />
                    ) : (
                        <div>Not shots found for this project</div>
                    )}
                    </>
                )}

                {activeTab === "assets" && (
                     <>
                    {assets && assets.length > 0 ? (
                    <Table columns={assetColumns} rows={assets} />
                    ) : (
                        <div>No assets found for this project</div>
                    )}
                    </>
                )}
            
            
                <div className="flex justify-center flex-row gap-1">
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded mt-4" title={"Delete project"} onClick={deleteProject}/>
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded mt-4" title={"Share project"} onClick={() => navigate(`/projects/${projectId}/share`)}/>
                </div>
             </div>
        </div>
    )
}