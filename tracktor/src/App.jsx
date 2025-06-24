import './App.css'
import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import {LandingPage} from './pages/landing_page.jsx'
import {CreateProjectPage} from './pages/create_project_page.jsx'
import { ProjectPage } from './pages/project_page.jsx'
import { Layout } from './pages/Layout.jsx'


function App() {

    return (
        <Router> 
            <Routes>
                <Route element={<Layout/>}>
                    <Route path="/" element={<LandingPage/>} />
                    <Route path="/create-project" element={<CreateProjectPage/>} />
                    <Route path="/project-name" element={<ProjectPage/>} />
                </Route>

            </Routes>
        </Router>
    )
  
}

export default App
