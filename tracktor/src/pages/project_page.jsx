import { useState, useEffect, act } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/Button";
import { StatusListbox } from "../components/StatusListbox";
import { Table } from "../components/Table";
import { Popup } from "../components/Popup";
import { Label } from "@headlessui/react";

export function ProjectPage({ reloadProjects }) {
    const { projectId } = useParams()
    const [project, setProject] = useState()
    const [shots, setShots] = useState()
    const [assets, setAssets] = useState()
    const [activeTab, setActiveTab] = useState("shots")
    const [popupOpen, setPopupOpen] = useState(false)
    const [popupFields, setPopupFields] = useState([])
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
            await axios.patch(`http://localhost:8080/api/projects/${projectId}/assets/${asset_id}`,
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

    const handleCreateClick = () => {
        if (activeTab === "shots") {
            setPopupFields([
                {name : "shot_name", label: "Shot Name", required: true}
            ])
        } else {
            setPopupFields([
                {name: "asset_name", label: "Asset Name", required: true},
                {name: "asset_type", label: "Asset Type", required: true}
            ])
        }
        setPopupOpen(true)
    }

    const handlePopupSubmit = async (formData) => {
        try {
            if (activeTab === "shots") {
                const response = await axios.post(`http://localhost:8080/api/projects/${projectId}/create_shot`, {
                    project_id: projectId,
                    shot_name: formData.shot_name
                })
                setShots([...shots, response.data])
            } else {
                const response = await axios.post(`http://localhost:8080/api/projects/${projectId}/create_asset`, {
                    project_id: projectId,
                    asset_name: formData.asset_name,
                    asset_type: formData.asset_type
            });
            setAssets([...assets, response.data]);
            }
            setPopupOpen(false)
        } catch (error) {
            alert("Failed to create item")
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
        { key: "asset_type", header: "Asset Type"},
        { key: "asset_status", header: "Status", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.asset_id, "asset_status", newStatus)}
            />
        )},
        { key: "prepro_status", header: "Pre-production", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.asset_id, "prepro_status", newStatus)}
            />
        )},
        { key: "mod_status", header: "Modelling", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.asset_id, "mod_status", newStatus)}
            />
        )},
        { key: "srf_status", header: "Surfacing", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.asset_id, "srf_status", newStatus)}
            />
        )},
        { key: "cfx_status", header: "CFX", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.asset_id, "cfx_status", newStatus)}
            />
        )},
        { key: "lit_status", header: "Lighting", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.asset_id, "lit_status", newStatus)}
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
                <div className="mt-5 mb-5 text-left">
                    <Button className={`px-4 py-2 rounded-t bg-gray-100 text-amber-800`}
                    onClick={handleCreateClick}
                    title={`${activeTab === "assets" ? "New Asset" : "New Shot" }`}/>
                </div>
                {activeTab === "shots" && (
                    <div>
                        
                        {shots && shots.length > 0 ? (
                        <Table columns={shotColumns} rows={shots} />
                        ) : (
                            <div>Not shots found for this project</div>
                        )}
                    </div>
                )}
                
                {activeTab === "assets" && (
                     <div>
                        {console.log("Assets:", assets)}
                        {assets && assets.length > 0 ? (
                        <Table columns={assetColumns} rows={assets} />
                        ) : (
                            <div>No assets found for this project</div>
                        )}
                    </div>
                )}
            
            
                <div className="flex justify-center flex-row gap-1">
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded mt-4" title={"Delete project"} onClick={deleteProject}/>
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded mt-4" title={"Share project"} onClick={() => navigate(`/projects/${projectId}/share`)}/>
                </div>
             </div>
             <Popup
                open={popupOpen}
                onClose={() => setPopupOpen(false)}
                onSubmit={handlePopupSubmit}
                fields={popupFields}
             />
        </div>
    )
}