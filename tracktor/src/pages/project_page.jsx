import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "../components/Button";
import { Popup } from "../components/Popup";
import { StatusListbox } from "../components/StatusListbox";
import { Table } from "../components/Table";

export function ProjectPage({ reloadProjects }) {
    const { projectId, username } = useParams()
    const [project, setProject] = useState()
    const [shots, setShots] = useState([])
    const [assets, setAssets] = useState([])
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
                    shot.id === shot_id ? {...shot, [field] : newStatus} : shot
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
                    asset.id === asset_id ? {...asset, [field] : newStatus} : asset
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

const statusColors = {
  "Not started": "bg-gray-200 text-gray-700",
  "WIP": "bg-blue-100 text-blue-700",
  "Ready to Review": "bg-orange-200 text-amber-700",
  "Complete": "bg-green-100 text-green-700",
  "Omitted" : "bg-red-100 text-red-700",
};


    const shotColumns = [
        { key: "shot_name", header: "Shot Name",
            render: (value, row) => (
                <span
                    className="underline text-amber-700 cursor-pointer"
                    role="button"
                    tabIndex={0}
                    onClick={() => navigate(`/${username}/projects/${projectId}/shots/${row.id}`)}
                    onKeyDown={e => (e.key === "Enter" || e.key === " ") && navigate(`/${username}/projects/${projectId}/shot/${row.id}`)}
                >
                {value}

                </span>
            )},
        { key: "status", header: "Status", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.id, "status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "lay_status", header: "Layout", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.id, "lay_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "anim_status", header: "Animation", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.id, "anim_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "cfx_status", header: "CFX", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.id, "cfx_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "lit_status", header: "Lighting", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateShotField(row.id, "lit_status", newStatus)}
                colourMap={statusColors}
            />
        )},
    ];

    const assetColumns = [
        { key: "asset_name", header: "Asset Name",
            render: (value, row) => (
                <span
                    className="underline text-amber-700 cursor-pointer"
                    role="button"
                    tabIndex={0}
                    onClick={() => navigate(`/${username}/projects/${projectId}/assets/${row.id}`)}
                    onKeyDown={e => (e.key === "Enter" || e.key === " ") && navigate(`/${username}/projects/${projectId}/assets/${row.id}`)}
                >
                {value}

                </span>
            )},
        { key: "asset_type", header: "Asset Type"},
        { key: "asset_status", header: "Status", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.id, "asset_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "prepro_status", header: "Pre-production", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.id, "prepro_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "mod_status", header: "Modelling", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.id, "mod_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "srf_status", header: "Surfacing", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.id, "srf_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "cfx_status", header: "CFX", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.id, "cfx_status", newStatus)}
                colourMap={statusColors}
            />
        )},
        { key: "lit_status", header: "Lighting", render: (value, row) => (
            <StatusListbox
                value={value}
                onChange={newStatus => updateAssetField(row.id, "lit_status", newStatus)}
                colourMap={statusColors}
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