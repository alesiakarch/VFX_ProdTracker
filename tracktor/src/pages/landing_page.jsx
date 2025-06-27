import { useState } from 'react'
import {Link} from 'react-router-dom'
import { Button } from '../components/Button'
import { useNavigate } from 'react-router-dom'




export function LandingPage() {
    
    const navigate = useNavigate();
    return (
        <div className = "flex flex-col space-y-4">
            <h1>Username's Projects</h1>
            <Button title ={"Project 1"} onClick ={() => navigate("/project-name")}/>
            <Button title ={"Project 2"} onClick ={() => navigate("/project-name")}/>
            <Button title = {"Create new project"} onClick={() => navigate("/create-project")}/>
        </div>
    );
}