import './App.css'
import { useState, useEffect } from 'react'
import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import {LandingPage} from './pages/landing_page.jsx'
import {CreateProjectPage} from './pages/create_project_page.jsx'
import { ProjectPage } from './pages/project_page.jsx'
import { Layout } from './pages/Layout.jsx'
import axios from 'axios'


function App() {

    const [projects, setProjects] = useState("")
    const [array, setArray] = useState([])
    const fetchAPI = async() => {
        const response = await axios.get("http://localhost:8080/api/users");
        setArray(response.data.users);
    }

    useEffect(() => {fetchAPI()}, [])
    return (
        <>
        <h1 className="text-3xl font-bold underline text-red-500">Hello Tailwind!</h1>
            {
            array.map((user, index) => (
                <div key={index}>
                <span>{user}</span>
                <br></br>
                </div>
            ))
            }
        <Router> 
            <Routes>
                <Route element={<Layout/>}>
                    <Route path="/" element={<LandingPage/>} />
                    <Route path="/create-project" element={<CreateProjectPage projects={projects} setProjects={setProjects}/>} />
                    <Route path="/project-name" element={<ProjectPage/>} />
                </Route>
                
            </Routes>
        </Router>
        </>
    )
  
}

export default App
