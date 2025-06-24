import { Link } from "react-router-dom"


export function Navbar() {
    return (
        <>
            <Link to="/">Home | </Link>
            <Link to="/create-project">Create a new project | </Link>
            <Link to="/project-name">Project-Name </Link>
        </>
    )
}