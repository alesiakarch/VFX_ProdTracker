import { useState, useEffect } from 'react'
import { Button } from '../components/Button'
import { useNavigate, useParams } from 'react-router-dom'
import axios from 'axios'

export function LandingPage({ projects, reloadProjects }) {
    
    const { username } = useParams()
    const navigate = useNavigate();
    const [assignedProjectIds, setAssignedProjectIds] = useState([])

    useEffect(() => {
        reloadProjects()
        const user_id = localStorage.getItem("user_id")
        if (user_id) {
            axios.get(`http://localhost:8080/api/usersProjects?user_id=${user_id}`)
                    .then(res => setAssignedProjectIds(res.data))
                    .catch(() => setAssignedProjectIds([]))

        }
    }, [reloadProjects])

    const userProjects = projects.filter(project => assignedProjectIds.includes(project.id))

    return (
        <div className = "flex items-center justify-center min-h-screen bg-amber-50">
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">{username}'s Projects</h1>
                <div className="flex justify-center flex-col gap-1">
                    {userProjects.map((project) => (
                        <Button className = "bg-amber-300 text-white mb-2 px-6 py-2 rounded" key={project.id} title={project.name} onClick={() => navigate(`/projects/${project.id}`)}/>
                    ))
                    }
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded"title = {"Create new project"} onClick={() => navigate(`/${username}/create-project`)}/>
                    <Button className="bg-amber-300 text-white mb-2 px-6 py-2 rounded" title = {"Add existing project"} onClick={() => navigate(`/${username}/projects/join`)}/>
                </div>
            </div>
        </div>
    );
}