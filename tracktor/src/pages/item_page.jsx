import axios from "axios"
import { useEffect, useState } from "react"
import { useNavigate, useParams, useSearchParams } from "react-router-dom"
import { Button } from "../components/Button"

export function ItemPage(){
    const {projectId, itemId, itemType, username} = useParams()
    const [item, setItem] = useState(null)
    const navigate = useNavigate()
    const [activeTab, setActiveTab] = useState("")
    const [searchParams, setSearchParams] = useSearchParams()

    const department = searchParams.get("department") || "All"

    const DEPARTMENTS = {
        shots: ["All", "lay", "anim", "cfx", "lit", "assets"],
        assets: ["All", "prepro", "mod", "srf", "cfx", "lit"]
    };

    const departments = DEPARTMENTS[itemType] || []

    useEffect(() => {
        const fetchItem = async () => {
            try {
                const item = await axios.get(`http://localhost:8080/api/projects/${projectId}/${itemType}/${itemId}`)
                setItem(item.data)
            } catch (error) {
                setItem(null)
            }
        }
        fetchItem()
    },[itemId, itemType])

    useEffect(() => {
    if (departments.length > 0) {
        setActiveTab(departments[0]);
    }
    }, [itemType]);

    if (!item) return <div>Loading...</div>;


    const handleTabChange = (dept) => {
        setSearchParams({department : dept})
        setActiveTab(dept)
    }

    const handleStatusClick = (dept) => {
        navigate(`/${username}/projects/${projectId}/${itemType}/${itemId}/${dept}/notes`)
    }
    console.log("itemType:", itemType, "departments:", departments);

    return (

        <div className="flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-screen">
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">
                {itemType === "shots"
                    ? `Shot name: ${item.shot_name || item.name}`
                    : `Asset name: ${item.asset_name || item.name}`}
                </h1>
                <div className="flex gap-2 mb-6">
                    {departments.map((dept) => (
                        <Button
                            key={dept}
                            className={`px-4 py-2 rounded-t ${activeTab === dept ? "bg-amber-300 text-white font-bold" : "bg-gray-100 text-amber-800"}`}
                            onClick={() => handleTabChange(dept)}
                            title={dept.toUpperCase()}
                        />

                    ))}
                </div>
                {activeTab && (
                    <div className="mb-4 text-left">
                        <Button
                            className={"px-4 py-2 rounded-t bg-amber-300 text-amber-700 font-bold"}
                            onClick={() => {handleStatusClick(activeTab)}}
                            title={`${activeTab.toUpperCase()} Notes`}
                        />
                    </div>
                )}
            </div>

        </div>

    )
}