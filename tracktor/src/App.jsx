import './App.css'
import { useState, useEffect, useCallback } from 'react'
import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import {LandingPage} from './pages/landing_page.jsx'
import {CreateProjectPage} from './pages/create_project_page.jsx'
import { ProjectPage } from './pages/project_page.jsx'
import { Layout } from './pages/layout.jsx'
import axios from 'axios'


function App() {

    const [projects, setProjects] = useState([])
    const [users, setUsers] = useState([])
    const fetchData = useCallback(async () => {
        try {
            const usersResponse = await axios.get("http://localhost:8080/api/users")
            setUsers(usersResponse.data.users)

            const projectsResponse = await axios.get("http://localhost:8080/api/projects")
            setProjects(projectsResponse.data)
        } catch (error) {
            setUsers([])
            setProjects([])
        }
    }, [])
    useEffect(() => {
        fetchData()
    }, [])
 
    return (
        <>
        <Router> 
            <Routes>
                <Route element={<Layout/>}>
                    <Route path="/" element={<LandingPage projects={projects} reloadProjects={fetchData} />} />
                    <Route path="/create-project" element={<CreateProjectPage projects={projects} setProjects={setProjects}/>} />
                    <Route path="/projects/:projectId" element={<ProjectPage />} />
                </Route>
                
            </Routes>
        </Router>
        </>
    )
  
}

export default App
