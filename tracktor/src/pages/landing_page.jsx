import { useState, useEffect } from 'react'
import { Button } from '../components/Button'
import { useNavigate, useParams } from 'react-router-dom'

export function LandingPage({ projects, reloadProjects }) {
    
    const { username } = useParams()
    const navigate = useNavigate();

    useEffect(() => {
        reloadProjects()
    }, [reloadProjects])

    return (
        <div className = "flex flex-col space-y-4">
            <h1>{username}'s Projects</h1>
            {projects.map((project, index) => (
                <Button key={project.id} title={project.name} onClick={() => navigate(`/projects/${project.id}`)}/>
            ))
            }
            <Button title = {"Create new project"} onClick={() => navigate("/create-project")}/>
            <Button title = {"Add existing project"} onClick={() => navigate("/add-project")}/>
        </div>
    );
}