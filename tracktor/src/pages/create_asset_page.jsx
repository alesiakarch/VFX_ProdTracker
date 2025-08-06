import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Textbox } from "../components/Textbox";
import { Button } from "../components/Button";

export function CreateAssetPage() {
    const [assetName, setAssetName] = useState("")
    const [assetType, setAssetType] = useState("")
    const { projectId} = useParams()
    const navigate = useNavigate()

    async function CreateAsset() {
        if (!assetName.trim()) return

        try {
            const response = await axios.post(`http://localhost:8080/api/projects/${projectId}/create_asset`, {
                asset_name : assetName,
                asset_type : assetType,
                project_id : projectId
            })
            navigate(`../`)
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
            alert("Failed to create asset")
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
                <h1 className="tet-3xl font-extrabold mb- text-center text-amber-700 drop-shadow">
                    Create Asset:
                </h1>
                <label className="flex items-center justify-center">
                    Asset name: 
                    <Textbox className={"ml-2 bg-gray-200 rounded"}
                    value={assetName}
                    onChange={(e) => setAssetName(e.target.value)}/>
                </label>
                <br></br>
                <label className="flex item-center justtify-center">
                    Asset type:
                    <Textbox className={"ml-2 bg-gray-200 rounded"}
                    value={assetType}
                    onChange={(e) => setAssetType(e.target.value)}/>
                </label>
                <Button className="mb-2 bg-amber-300 text-white px-4 py-2 rounded mt-2"
                title={"Create Asset"}
                onClick={CreateAsset}/>
            </div>
        </div>
    )
}