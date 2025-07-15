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
        <div className="flex flex-col space-y-4">
            {sharecode && <h1>Sharecode: {sharecode}</h1>}
            <Button title={"Share project"} onClick={GenerateSharecode}/>
        </div>
    )
}