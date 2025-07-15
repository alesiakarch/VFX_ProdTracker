import './App.css'
import { useState, useEffect, useCallback } from 'react'
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import {LandingPage} from './pages/landing_page.jsx'
import {CreateProjectPage} from './pages/create_project_page.jsx'
import { ProjectPage } from './pages/project_page.jsx'
import { Layout } from './pages/layout.jsx'
import { LoginPage } from './pages/login_page.jsx'
import axios from 'axios'
import { ShareProjectPage } from './pages/share_project_page.jsx'
import { JoinProjectPage } from './pages/join_project_page.jsx'


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
                    <Route path ="/:username/projects" element={<LandingPage projects={projects} reloadProjects={fetchData}/>}/>
                    <Route path="/" element={<LoginPage />} />
                    <Route path="/create-project" element={<CreateProjectPage projects={projects} setProjects={setProjects}/>} />
                    <Route path="/projects/:projectId" element={<ProjectPage />} />
                    <Route path="/projects/:projectId/share" element={<ShareProjectPage/>} />
                    <Route path="/:username/projects/join" element={<JoinProjectPage/>} />
                </Route>
            </Routes>
        </Router>
        </>
    )
}

export default App
