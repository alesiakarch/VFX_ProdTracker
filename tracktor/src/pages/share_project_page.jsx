import axios from "axios"
import { Button } from "../components/Button"   
import { useParams } from "react-router-dom"
import { useState } from "react"


export function ShareProjectPage() {
    const { projectId } = useParams()
    const [sharecode, setSharecode] = useState()

    async function GenerateSharecode() {
        try {
            const response = await axios.get(`http://localhost:8080/api/projects/${projectId}/share`)
            setSharecode(response.data.sharecode)
        } catch (error) {
            alert("Failed to generate sharecode")
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-amber-50">
        <div className="bg-white shadow-lg rounded p-8 w-full max-w-screen">
            <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">
                Press the button to generate the project code and share it with your teammates
            </h1>
            {sharecode && <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-500 drop-shadow">
                Sharecode: {sharecode}</h1>}
            <Button className="bg-amber-300 text-white px-4 py-2 rounded mt-2" title={"Share project"} onClick={GenerateSharecode}/>
        </div>    
        </div>
    )
}