import './App.css'
import { useState } from 'react'
import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import {LandingPage} from './pages/landing_page.jsx'
import {CreateProjectPage} from './pages/create_project_page.jsx'
import { ProjectPage } from './pages/project_page.jsx'
import { Layout } from './pages/Layout.jsx'


function App() {

    const [projects, setProjects] = useState("")
    return (
        <>
        <h1 className="text-3xl font-bold underline text-red-500">Hello Tailwind!</h1>
        <Router> 
            <Routes>
                <Route element={<Layout/>}>
                    <Route path="/" element={<LandingPage/>} />
                    <Route path="/create-project" element={<CreateProjectPage/>} />
                    <Route path="/project-name" element={<ProjectPage/>} />
                </Route>
                
            </Routes>
        </Router>
        </>
    )
  
}

export default App
