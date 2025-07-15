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
        <div className = "flex flex-col space-y-4">
            <h1>{username}'s Projects</h1>
            {userProjects.map((project) => (
                <Button key={project.id} title={project.name} onClick={() => navigate(`/projects/${project.id}`)}/>
            ))
            }
            <Button title = {"Create new project"} onClick={() => navigate(`/${username}/create-project`)}/>
            <Button title = {"Add existing project"} onClick={() => navigate(`/${username}/projects/join`)}/>
        </div>
    );
}